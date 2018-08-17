#!/usr/env python 3
import pygal
import flask
import json
import os
import logging
import sqlite3 as db
import time
from datetime import datetime
from urllib.request import urlopen
from flask import Flask, render_template, request
from pygal.style import DarkSolarizedStyle

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


# Reads data from temp/humidity database
def readData(timestamp, temp, humidity):
    try: 
        conn = db.connect(tempds)
        cursStamp = conn.cursor()
        cursTemp = conn.cursor()
        cursHum = conn.cursor()
        cursStamp.execute(
            "SELECT timestamp FROM ASSIGNMENT1_data values(?,)", timestamp)
        cursTemp.execute(
            "SELECT temp FROM ASSIGNMENT1_data values(?,)", temp)
        cursHum.execute(
            "SELECT humidity FROM ASSIGNMENT1_data values(?,)", humidity)

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
        'humidity' : humidity
	}
	return render_template('index.html', **templateData)

if __name__ == "__main__":
	host = os.popen('hostname -I').read()
	app.run(host=host, port=80, debug=False)
