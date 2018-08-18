#!/usr/bin/env python3
import pygal
import os
import logging
import sqlite3 as db
from flask import Flask, render_template, request
from time import sleep
from shutil import copy2


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
                "SELECT * FROM ASSIGNMENT1_data ORDER BY timestamp DESC\
                 LIMIT 1"):
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
@app.route("/graphs")
getLinegraph():
    try:
        line_chart = pygal.Line()
        line_chart.title = 'Temperature & Humidity Data over time'
        line_chart.x_labels = map(str, range(2002, 2013))
        line_chart.add('Temperature', [None, None,    0, 16.6,   25,   31, 36.4, 45.5, 46.3, 42.8, 37.1])
        line_chart.add('Humidity',  [None, None, None, None, None, None,    0,  3.9, 10.8, 23.8, 35.3])
        line_chart.render()
    return render_template('linegraph.html', templates)
    except Exception, e:
        return(str(e))


# Main routine - Design taken from week 5 code samples  
@app.route("/")
def index():
    timestamp, temp, humidity = readData()
    templateData = {
        'Timestamp': timestamp,
        'Temperature': temp,
        'Humidity': humidity
    }
    return render_template('index.html', **templateData)


if (__name__ == "__main__"):
    host = os.popen('hostname -I').read()
    app.run(host=host, port=8080, debug=False)
