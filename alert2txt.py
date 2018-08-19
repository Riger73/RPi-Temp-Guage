#!/usr/bin/env python3
from time import sleep
import requests
import json
import os
import sqlite3 as db

# Author Tim Novice sn: s3572290 RMIT
#
# Sends text alerts when temperature dips below 10 degrees.
# Uses Pushbullet as text service.
# Code leverages week 4 and 5 tutorial material - specifically
# "96_pycurlBullet.py".
# Must be in the same directory as 'temp_guage.py'
#

ACCESS_TOKEN = "o.9ClLiy99ubTKdvpdz9jmCqemdKq8sx9h"
tempds = '/database/a1data.db'


# Read data from database - includes temperature and timestamp
def getTemp():
    try:
        conn = db.connect(tempds)
        curs = conn.cursor()
        for row in curs.execute(
                "SELECT * FROM ASSIGNMENT1_data ORDER BY timestamp DESC LIMIT\
                 1"):
            timestamp = str(row[0])
            temp = row[1]
            return (timestamp, temp)
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


def main():
    timestamp, temp = getTemp()
    if (temp < 20):
        ip_address = os.popen('hostname -I').read()
        alerttexter(
            ip_address,
            "Alert: Temperature From Raspberry Pi is below 20 degrees C! %s%s"
            % (timestamp, temp))


main()