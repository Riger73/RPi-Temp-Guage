#!/usr/bin/env python3
from sense_hat import SenseHat
from datetime import datetime
from time import sleep
from threading import Timer
import datetime
import sqlite3 as db
import sys

# Author Tim Novice sn: s3572290 RMIT
#
# Gathers temerature and offsets from device heat.
# Returns calibrated temerature and date time
# Cycles through periodically until receiving exit feed
# To be used as a cron task.
#
sense = SenseHat()
sense.clear()

tempds = '/database/a1data.db'


# Write data to database
def logData(timestamp, temp, humidity):
    try:
        params = (timestamp, temp, humidity)
        conn = db.connect(tempds)
        curs = conn.cursor()
        curs.execute("INSERT INTO ASSIGNMENT1_data values(?, ?, ?)", params)
    except db.OperationalError as e:
        if ("locked" in str(e)):
            sleep(1)
        else:
            raise
    except KeyboardInterrupt:
        conn.commit()
        conn.close()
        conn.interrupt()
    finally:
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
    if (temp and humidity is not None):
        rawtime = datetime.datetime.now()
        melbtime = rawtime + datetime.timedelta(hours=10)
        timestamp = melbtime.strftime("%H:%M")
        # Approximate cpu temperature load accounted for
        temp = round(temp, 1) - 20
        humidity = round(humidity, 1)
        logData(timestamp, temp, humidity)


# Implements thread to poll persistently as a recursion
def poll():
    getTempData()
    t = Timer(0.3, poll)
    t.start()


# Main method to handle entrypoint for thread to poll every 3 milliseconds
# Effectively functions as a main().
def main():
    try:
        t = Timer(0.3, poll)
        t.start()
    except KeyboardInterrupt:
        sense.clear()
        print("Thread closed")
        sys.exit()
main()
