#!/usr/env python 3
import pygal
import json
import sqlite3 as db
from urllib.request import urlopen
from flask import Flask
from pygal.style import DarkSolarizedStyle

app = Flask(__name__)
tempds = '/database/a1data.db'
dbfile = 'a1data.db'
dbfilePath = '/database/a1data.db'

# Reads data from temp/humidity database
def readData(timestamp, temp, humidity):
    try: 
        params = (timestamp, temp, humidity)
        conn = db.connect(tempds)
        curs = conn.cursor()
        curs.execute("SELECT FROM ASSIGNMENT1_data values(?, ?, ?)", params)
    # Handles db locking
    except db.OperationalError as e:
        if ("locked" in str(e)):
            sleep(1)
        else:
            raise
    finally:
        conn.commit()
        conn.close()