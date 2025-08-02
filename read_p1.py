#!/usr/bin/python3
import traceback

# This script will read data from serial connected to the digital meter P1 port

# Created by Jens Depuydt
# https://www.jensd.be
# https://github.com/jensdepuydt

import serial
import crcmod.predefined
import psycopg2
import re
from datetime import datetime
import pytz

timezone = pytz.timezone('Europe/Brussels')
schema="public"
table="telegram"
obiscodes = {
    #Timestamp
    "0-0:1.0.0": {"previous":"", "current":""},
    #Day rate ext
    "1-0:1.8.1": {"previous":"", "current":""},
    #Day rate int
    "1-0:2.8.1": {"previous":"", "current":""},
    #Night rate ext
    "1-0:1.8.2": {"previous":"", "current":""},
    #Night rate ext
    "1-0:2.8.2": {"previous":"", "current":""},
    # extract second
    "1-0:1.7.0": {"previous":"", "current":""},
    # inject second
    "1-0:2.7.0": {"previous":"", "current":""},

    #Tabel piek maand extraction
    "1-0:1.6.0": {"previous":"", "current":""},
    #Tabel gas
    "0-1:24.2.3": {"previous":"", "current":""},
    #Tabel water
    "0-2:24.2.1": {"previous":"", "current":""}
}
# Change your serial port here:
#serialport = '/dev/ttyUSB0'
serialport = 'COM3'

# Enable debug if needed:
debug = True

def checkcrc(p1telegram):
    # check CRC16 checksum of telegram and return False if not matching
    # split telegram in contents and CRC16 checksum (format:contents!crc)
    for match in re.compile(b'\r\n(?=!)').finditer(p1telegram):
        p1contents = p1telegram[:match.end() + 1]
        # CRC is in hex, so we need to make sure the format is correct
        givencrc = hex(int(p1telegram[match.end() + 1:].decode('ascii').strip(), 16))
    # calculate checksum of the contents
    calccrc = hex(crcmod.predefined.mkPredefinedCrcFun('crc16')(p1contents))
    # check if given and calculated match
    if debug:
        print(f"Given checksum: {givencrc}, Calculated checksum: {calccrc}")
    if givencrc != calccrc:
        if debug:
            print("Checksum incorrect, skipping...")
        return False
    return True

def createTableSQL():
    sql="""
        CREATE TABLE {tableschema}."{tablename}" (
                                                     ts timestamp with time zone NOT NULL,
                                                     value numeric(10,3) NOT NULL,
            CONSTRAINT "{tablename}_pk" PRIMARY KEY (ts)
            );
        """
    #        COMMENT ON TABLE public."{tablename}" IS "{tablecomment}";
    for obis in obiscodes:
        if obis!="0-0:1.0.0":
            #        print(sql.format(tablename=obis, tablecomment=obiscodes[obis]["comment"]))
            executeSQL(sql.format(tableschema=schema,tablename=obis))

def executeSQL(sql):
    try:
        conn = psycopg2.connect(
            database="postgres",
            user="postgres",
            password="example",
            host="localhost",
            port="5432"
        )
        cur = conn.cursor()
        cur.execute(sql)
        print(sql)
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn:
            conn.close()
            print("Database connection closed.")

def processTelegramLine(line):
    print("Processing " + line)
    obis = line.split("(")[0]
    if obis in obiscodes:
        obiscodes[obis]["current"] = re.findall(r'\(.*?\)', line)
        print("Processed: "+ obis + " with value " + str(obiscodes[obis]["current"]))


def processObisCodes():
    sql= """
         insert into {tableschema}."{tablename}"
         values('{ts}', {value}); \
         """
    for obis in obiscodes:
        if obis!="0-0:1.0.0":
            if obiscodes[obis]["current"]!= obiscodes[obis]["previous"]:
                # change of data, so store in db
                if len(obiscodes[obis]["current"]) == 1:
                    ts= obiscodes["0-0:1.0.0"]["current"][0]
                    value=obiscodes[obis]["current"][0]
                else:
                    ts=obiscodes[obis]["current"][0]
                    value=obiscodes[obis]["current"][1]
                if ts[-2:-1]=="S":
                    is_dst_val=True
                else:
                    is_dst_val=False
                value=value[1:value.find('*')]
                executeSQL(sql.format(tableschema=schema,tablename=obis,ts=str(timezone.localize(datetime.strptime(ts[1:-2],'%y%m%d%H%M%S'),is_dst=is_dst_val)) ,value=value))
                obiscodes[obis]["previous"]=obiscodes[obis]["current"]

def processTelegram(telegram):
    for line in telegram.split(b'\r\n'):
        processTelegramLine(line.decode('ascii'))
    processObisCodes()
    print(obiscodes["1-0:1.7.0"]["current"][0] + ' ' + obiscodes["1-0:2.7.0"]["current"][0])


def main():
    ser = serial.Serial(serialport, 115200, xonxoff=1)
    p1telegram = bytearray()
    createTableSQL()
    while True:
        try:
            # read input from serial port
            p1line = ser.readline()
            if debug:
                print ("Reading: ", p1line.strip())
            # P1 telegram starts with /
            # We need to create a new empty telegram
            if "/" in p1line.decode('ascii'):
                if debug:
                    print ("Found beginning of P1 telegram")
                p1telegram = bytearray()
                print('*' * 60 + "\n")
            # add line to complete telegram
            p1telegram.extend(p1line)
            # P1 telegram ends with ! + CRC16 checksum
            if "!" in p1line.decode('ascii'):
                if debug:
                    print("Found end, printing full telegram")
                    print('*' * 40)
                    print(p1telegram.decode('ascii').strip())
                    print('*' * 40)
                if checkcrc(p1telegram):
                    # parse telegram contents, line by line
                    processTelegram(p1telegram)
        except KeyboardInterrupt:
            print("Stopping...")
            ser.close()
            break
        except:
            if debug:
                print(traceback.format_exc())
            # print(traceback.format_exc())
            print ("Something went wrong...")
            ser.close()
        # flush the buffer
        ser.flush()

if __name__ == '__main__':
    main()