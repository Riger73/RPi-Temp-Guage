#!/usr/bin/env python3
import sqlite3 as db

# Author - Tim Novice sn: s3572290 RMIT
#
# Code adapted from tutorial 4 examples using 'with' keyword.
# Utility to create adhoc database.
#

conn = db.connect('bta1data.db')
with conn:
    curs = conn.cursor()
    curs.execute("DROP TABLE IF EXISTS BT_data")
    curs.execute(
        "CREATE TABLE BT_data(user_name CHAR, device_name CHAR)")
