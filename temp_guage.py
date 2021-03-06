#!/usr/bin/env python3
from sense_hat import SenseHat
from datetime import datetime
from time import sleep
from threading import Timer
import datetime
import requests
import json
import os
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
ACCESS_TOKEN = "o.9ClLiy99ubTKdvpdz9jmCqemdKq8sx9h"


# Method to use PushBullet to send text alerts when the temperature
# drops below 10.
def alerttexter(title, body):
    """ Sending notification via pushbullet.
        Args:
            title (str) : title of text.
            body (str) : Body of text.
    """
    data_send = {"type": "note", "title": title, "body": body}

    resp = requests.post(
        'https://api.pushbullet.com/v2/pushes', data=json.dumps(data_send),
        headers={
            'Authorization': 'Bearer ' + ACCESS_TOKEN, 'Content-Type':
            'application/json'
        }
    )
    if resp.status_code != 200:
        raise Exception(
            'SomeAlert message was attempted but failed to connect')
    else:
        print('complete sending')


# Write data to database
def logData(timestamp, temp, humidity):
    try:
        params = (timestamp, temp, humidity)
        conn = db.connect(tempds)
        curs = conn.cursor()
        curs.execute("INSERT INTO ASSIGNMENT1_data values(?, ?, ?)", params)
    # Handles db locking
    except db.OperationalError as e:
        if ("locked" in str(e)):
            sleep(1)
        else:
            raise
    except KeyboardInterrupt:
        conn.commit()
        conn.close()
        # Kill db connection in case close() gets locked up
        conn.interrupt()
    finally:
        conn.commit()
        conn.close()


# Temperature and humitity poller
def getTempData():
    temp = sense.get_temperature()
    humidity = sense.get_humidity()

    sense.clear()
    if (temp and humidity is not None):
        rawtime = datetime.datetime.now()
        melbtime = rawtime + datetime.timedelta(hours=10)
        timestamp = melbtime.strftime("%H:%M")
        # Approximate cpu temperature load accounted for
        temp = round(temp, 1) - 18
        humidity = round(humidity, 1)
        logData(timestamp, temp, humidity)
        if (temp < 20):
            ip_address = os.popen('hostname -I').read()
            alerttexter(
                ip_address,
                "Alert: Temperature From Raspberry Pi is below 20 degrees C!")
        sense.clear()
        sense.show_message(
            'Temp: {0:0.1f} *c'.format(temp), scroll_speed=0.03)
        sense.clear()


# Implements thread, polling persistently.
def poll():
    getTempData()
    t = Timer(0.3, poll)
    t.start()


# Main method to handle entrypoint for polling thread
def main():
    try:
        poll()
    except KeyboardInterrupt:
        sense.clear()
        print("Thread closed")
        sys.exit()


main()
