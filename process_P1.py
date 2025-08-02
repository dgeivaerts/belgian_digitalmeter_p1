import psycopg2
import re
from datetime import datetime
import time
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

global conn

