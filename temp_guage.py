#!/usr/bin/env python3
import sys
from sense_hat import SenseHat
from datetime import datetime
from threading import Timer
import sqlite3 as db
from threading import Thread

# Author Tim Novice sn: s3572290 RMIT
#
# Gathers temerature and offsets from device heat.
# Returns calibrated temerature and date time
# Cycles through periodically until receiving exit feed
# To be used as a cron task.
# Place in same directory as database.
#
sense = SenseHat()
sense.clear()

tempds = 'a1data.db'

# Write data to database
def logData(timestamp, temp, humidity):
    params(timestamp, temp, humidity)
    conn = db.connect(tempds)
    curs=conn.cursor()
    curs.execute("INSERT INTO ASSIGNMENT1_data values(?, ?, ?)", params)
    conn.commit()
    conn.close()

# Temperature and humitity poller
def getTempData():    
    temp = sense.get_temperature()
    humidity = sense.get_humidity()
    sense.show_message(
        'Temp: {0:0.1f} *c'.format(temp), scroll_speed = 0.05)
    sense.clear()
    sense.show_message(
        'Humidity: {0:0.1f} *c'.format(humidity), scroll_speed = 0.05)
    sense.clear()
    if temp & humidity is not None:
        timestamp = datetime.now().strftime("%H:%M")
        temp = round(temp, 1)
        humidity = round(humidity, 1)
        logData(timestamp, temp, humidity)

# Thread to recursively poll every 5 milliseconds, and calls processes.
def poll():
    try:
        getTempData()
        t = Timer(0.5, poll)
        t.daemon = True
        t.start()
    except KeyboardInterrupt:
        sense.clear()
        print("Thread closed").exit()

def main():
    try: 
        # Calls a thread timer to initiate the poll
        t = Timer(0.5, poll)
        t.daemon = True
        t.start()
    except KeyboardInterrupt:
        sense.clear()
        print("Thread closed").exit()

main()
