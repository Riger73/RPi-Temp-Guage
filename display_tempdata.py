#!/usr/env python 3
import pygal
import flask
import json
import os
from datetime import datetime
import sqlite3 as db
from urllib.request import urlopen
from flask import Flask, render_template, request
from pygal.style import DarkSolarizedStyle

# Author Tim Novice sn: s3572290 RMIT
#
# Retrieves data from database and populates it to
# a web server page. Week 5 tutorial and sample code
# were used to build the web server. 
#

tempds = '/database/a1data.db'

# Reads data from temp/humidity database
def readData(timestamp, temp, humidity):
    try: 
        params = (timestamp, temp, humidity)
        conn = db.connect(tempds)
        curs = conn.cursor()
        curs.execute("SELECT FROM ASSIGNMENT1_data values(?, ?, ?)", params)

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


# Main routine - Design taken from week 6 code samples  
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
