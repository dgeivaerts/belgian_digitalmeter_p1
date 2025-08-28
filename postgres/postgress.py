import datetime
import json
from decimal import Decimal
from json import JSONEncoder

import psycopg2

def executeSQL(sql):
    try:
        conn = psycopg2.connect(
            database="postgres",
            user="postgres",
            password="postgres",
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

def fetchPower():
    try:
        conn = psycopg2.connect(
            database="postgres",
            user="postgres",
            password="example",
            host="localhost",
            port="5432"
        )
        cur = conn.cursor()
        cur.execute("select power from public.omnikpower where ts = (select max(ts) from public.omnikpower)")
        power = cur.fetchone()[0]
        print(power)
        cur.close()
        return power
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn:
            conn.close()
            print("Database connection closed.")

def fetchPowerToday():
    try:
        conn = psycopg2.connect(
            database="postgres",
            user="postgres",
            password="example",
            host="localhost",
            port="5432"
        )
        cur = conn.cursor()
        cur.execute("select ts, power  from public.omnikpower where date(ts)=date(now())")
        power = cur.fetchall()
        cur.close()
        return json.dumps(power,cls=DateTimeEncoder)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn:
            conn.close()
            print("Database connection closed.")

class DateTimeEncoder(JSONEncoder):
    #Override the default method
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()

if __name__ == "__main__":
    print(fetchPowerToday())