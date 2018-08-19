#!/usr/bin/env python3
import os
import sqlite3 as db
import pygal
from flask import Flask, render_template
from pygal.style import LightSolarizedStyle
from shutil import copy2
from time import sleep

# Author Tim Novice sn: s3572290 RMIT
#
# Retrieves data from database and populates it to
# a web server page. Week 5 tutorial and sample code
# were used to build the web server.
#

app = Flask(__name__)


dbfilePath = '/database/a1data.db'
cachefile = '/database/a1data_cache.db'


# Reads data from the database to populate the web
def readData():
    try:
        if(os.path.isfile(cachefile)):
            os.remove(cachefile)
        copy2(dbfilePath, cachefile)
        conn = db.connect(cachefile)
        curs = conn.cursor()
        curs.execute(
                "SELECT * FROM ASSIGNMENT1_data ORDER BY timestamp DESC LIMIT 10")
        dbData = curs.fetchall()
        timestamps = []
        temps = []
        humiditys = []
        for row in reversed(dbData):
            timestamps.append(row[0])
            temps.append(row[1])
            humiditys.append(row[2])    
        conn.close()
        return timestamps, temps, humiditys
    # Handles db locking
    except db.OperationalError as e:
        if ("locked" in str(e)):
            sleep(1)
        else:
            raise


# Method using Pygal libraries to plot line graphs
# Code samples sourced from www.pygal.org
@app.route("/")
def getLinegraph():
    timestamps, temps, humiditys = readData()
    try:
        linegraph = pygal.StackedLine(
            fill=True, interpolate='cubic', style=LightSolarizedStyle)
        linegraph.title = 'Temperature & Humidity Data over time'
        linegraph.x_labels = map(str, timestamps)
        linegraph.add('Temperature', temps)
        linegraph.add('Humidity', humiditys)
        return linegraph.render_response()
    except Exception as e:
        return(str(e))


# Main routine - Design taken from week 5 code samples
def index():
    getLinegraph()


if (__name__ == "__main__"):
    host = os.popen('hostname -I').read()
    app.run(host=host, port=8080, debug=False)
