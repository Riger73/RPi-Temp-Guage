#!/usr/bin/env python3
import os
import pyodbc as db
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


# Reads data from the database to populate the web
def readData():
    try:
        conn = db.connect('Driver={SQL Server};'
                          'Server=localhost;'
                          'Database=testdb;'
                          'uid=sa;pwd=P@ssw0rd')
        curs = conn.cursor()
        curs.execute(
                "SELECT * FROM PMReport ORDER BY timestamp DESC\
                 LIMIT 10")
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
        line_chart = pygal.HorizontalBar(
            fill=True, interpolate='cubic', style=LightSolarizedStyle)
        line_chart.title = 'Temperature & Humidity Data over time'
        line_chart.x_labels = map(str, timestamps)
        line_chart.add('Temperature', temps)
        line_chart.add('Humidity', humiditys)
        return line_chart.render_response()
    except Exception as e:
        return(str(e))


# Main routine - Design taken from week 5 code samples
def index():
    getLinegraph()


if (__name__ == "__main__"):
    host = os.popen('hostname -I').read()
    app.run(host=host, port=8080, debug=False)
