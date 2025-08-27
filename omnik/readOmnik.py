import socket
from datetime import timezone, datetime

import pytz

from omnik import InverterMsg
from postgres.postgress import executeSQL

device_serial_number = 1606720080
ip = '192.168.1.220'
port = 8899
time_out = 10
e_today = 0
timezone = pytz.timezone('Europe/Brussels')

def generate_buffer(device_serial_number):
    """
    The request string is build from several parts. The first part is a
    fixed 4 char string; the second part is the reversed hex notation of
    the Wi-Fi logger s/n twice; then again a fixed string of two chars; a checksum of
    the double s/n with an offset; and finally a fixed ending char.
    this code requires python 3.5 or later!
    """
    responseString = b"\x68\x02\x40\x30"
    doublehex = hex(device_serial_number)[2:] * 2
    hexlist = [
        bytes.fromhex(doublehex[i : i + 2])
        for i in reversed(range(0, len(doublehex), 2))
    ]
    cs_count = 115 + sum([ord(c) for c in hexlist])
    cs = bytes.fromhex(hex(cs_count)[-2:])
    responseString += b"".join(hexlist) + b"".join([b"\x01\x00", cs, b"\x16"])
    return responseString

def toString(msg):
    if msg is None:
        print("No data received from call.")
    else:
        print("ID: {0}".format(msg.id))
        print("E Today: {}   Total: {}".format(msg.e_today, msg.e_total))
        print("Power generating {}".format(msg.p_ac(1)))

def makeCall():
    for res in socket.getaddrinfo(ip, port, socket.AF_INET,socket.SOCK_STREAM):
        family, socktype, proto, canonname, sockadress = res
        try:
            inverter_socket = socket.socket(family, socktype, proto)
            inverter_socket.settimeout(time_out)
            inverter_socket.connect(sockadress)
            inverter_socket.sendall(generate_buffer(device_serial_number))
            data = inverter_socket.recv(1024)
            inverter_socket.close()
            msg = InverterMsg.InverterMsg(data)
            process_omnik_msg(msg)
            return msg
        except socket.error as msg:
    #        sys.exit(1)
            print('Connectiviy issue with inverter')
            return None

def process_omnik_msg(msg):
    global e_today
    ts=str(datetime.now(timezone))
    sql= """insert into public.omnikPower values('{ts}',{power});"""
    executeSQL(sql.format(ts=ts, power=msg.p_ac(1)))
    if msg.e_today!=e_today:
        sql= """insert into public.omnik values('{ts}', {today},{total});"""
        executeSQL(sql.format(ts=ts, today=msg.e_today , total=msg.e_total))
        e_today=msg.e_today

def run():
    while True:
        toString(makeCall())

if __name__ == "__main__":
    e_today=0
    run()