#!/usr/bin/env python3
import pygal
import os
import logging
import sqlite3 as db
from flask import Flask, render_template, request
from time import sleep


# Author Tim Novice sn: s3572290 RMIT
#
# Retrieves data from database and populates it to
# a web server page. Week 5 tutorial and sample code
# were used to build the web server. 
#

app = Flask(__name__)

# Testing logging, to remove when live
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

tempds = '/database/a1data.db'


# Reads data from the database to populate the web
def readData():
    try:
        conn = db.connect(tempds)
        curs = conn.cursor()
        while (curs.execute(
                "SELECT * FROM ASSIGNMENT1_data ORDER BY timestamp DESC\
                 LIMIT 1") is not None):
            for row in curs.execute(
                    "SELECT * FROM ASSIGNMENT1_data ORDER BY timestamp DESC\
                     LIMIT 1"):
                timestamp = str(row[0])
                temp = row[1]
                humidity = row[2]
            return timestamp, temp, humidity
    # Handles db locking
    except db.OperationalError as e:
        if ("locked" in str(e)):
            sleep(1)
        else:
            raise
    finally:
        conn.commit()
        conn.close()


# Main routine - Design taken from week 5 code samples  
@app.route("/")
def index():	
    timestamp, temp, humidity = readData()
    templateData = {
        'timestamp': timestamp,
        'temp': temp,
        'humidity': humidity
    }
    return render_template('index.html', **templateData)


if (__name__ == "__main__"):
    host = os.popen('hostname -I').read()
    app.run(host=host, port=8080, debug=False)
