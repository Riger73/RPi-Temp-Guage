#!/usr/bin/env python3
import logging
import os
import sqlite3 as db
from shutil import copy2
from time import sleep

import pygal
from flask import Flask, render_template
from pygal.style import LightSolarizedStyle

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
cachefile = '/database/a1data_cache.db'


# Reads data from the database to populate the web
def readData():
    try:
        if(os.path.isfile(cachefile)):
            os.remove(cachefile)
        copy2(tempds, cachefile)
        conn = db.connect(cachefile)
        curs = conn.cursor()
        for row in curs.execute(
                "SELECT * FROM ASSIGNMENT1_data ORDER BY timestamp DESC"):
            timestamp = str(row[0])
            temp = row[1]
            humidity = row[2]
        conn.close()
        return timestamp, temp, humidity
    # Handles db locking
    except db.OperationalError as e:
        if ("locked" in str(e)):
            sleep(1)
        else:
            raise


# Method using Pygal libraries to plot line graphs
@app.route("/templates/")
def getLinegraph():
    timestamp, temp, humidity = readData()
    templateData = {
        'Timestamp': timestamp,
        'Temperature': temp,
        'Humidity': humidity
    }
    try:
        linegraph = pygal.StackedLine(
            fill=True, interpolate='cubic', style=LightSolarizedStyle)
        linegraph.title = 'Temperature & Humidity Data over time'
        for timestamp in templateData:
            linegraph.x_labels = map(str, timestamp)
        for temp in templateData:
            linegraph.add('Temperature', temp)
        for humidity in templateData:
            linegraph.add('Humidity',  humidity)
        return render_template("index.html", **linegraph.render_data_uri())
    except Exception as e:
        return(str(e))


# Main routine - Design taken from week 5 code samples
@app.route("/")
def index():
    getLinegraph()


if (__name__ == "__main__"):
    host = os.popen('hostname -I').read()
    app.run(host=host, port=8080, debug=False)
