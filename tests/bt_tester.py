#!/usr/bin/env python3
import sys
import bluetooth
import os
import time
import sqlite3 as db
from sense_hat import SenseHat
from time import sleep

# Author Tim Novice sn: s3572290 RMIT
#
# Adapted code from Week 5 tutorial task 'findmyphone.py'.
# Pairs to a know Bluetooth device and sends weather notifications.
#

userds = '/database/a1data.db'


# Write bt details to database
def setBtData(user_name, device_name):
    try:
        params = (user_name, device_name)
        conn = db.connect(userds)
        curs = conn.cursor()
        curs.execute("INSERT INTO BT_data values(?, ?)", params)
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


# Searches database for bt details and then tries to pair
def getBtData():
    try:
        conn = db.connect(userds)
        curs = conn.cursor()
        curs.execute(
                "SELECT * FROM BT_data ORDER BY user_name DESC LIMIT 1")
        dbData = curs.fetchall()
        user_name = []
        device_name = []
        if (dbData is not None):
            for row in reversed(dbData):
                user_name.append(row[0])
                device_name.append(row[1])
        conn.close()
        return user_name, device_name
    # Handles db locking
    except db.OperationalError as e:
        if ("locked" in str(e)):
            sleep(1)
        else:
            raise


# Search for device based on device's name
def search(user_name, device_name):
    try:
        while True:
            device_address = None
            dt = time.strftime("%a, %d %b %y %H:%M:%S", time.localtime())
            print("\nCurrently: {}".format(dt))
            time.sleep(3)
            nearby_devices = bluetooth.discover_devices()
            for mac_address in nearby_devices:
                if device_name == bluetooth.lookup_name(
                        mac_address, timeout=5):
                    device_address = mac_address
                    break
            if device_address is not None:
                print(
                    "Hi {}! Your phone ({}) has the MAC address: {}".format(
                        user_name, device_name, device_address))
                sense = SenseHat()
                temp = round(sense.get_temperature(), 1)
                sense.show_message(
                    "Hi {}! The Current Temp is {}*c".format(
                        user_name, temp), scroll_speed=0.05)
            else:
                print("No device located in range ...")
    except KeyboardInterrupt:
        print("Bluetooth disconnected")
        sys.exit()


# Main method
def main():
    # user_name, device_name = getBtData()
    user_name = input("Enter your name: ")
    device_name = input("Enter the name of your phone: ")
    setBtData(user_name, device_name)
    search(user_name, device_name)


main()
