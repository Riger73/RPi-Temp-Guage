#!/usr/bin/env python3
import requests
import json
import os

# Author Tim Novice sn: s3572290 RMIT
#
# Sends text alerts when temperature dips below 10 degrees.
# Uses Pushbullet as text service.
# Code leverages week 4 and 5 tutorial material - specifically
# "96_pycurlBullet.py".
#

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


# main function
def main():
    ip_address = os.popen('hostname -I').read()
    alerttexter(
        ip_address,
        "Alert: Temperature From Raspberry Pi is below 10 degrees C!")


main()
