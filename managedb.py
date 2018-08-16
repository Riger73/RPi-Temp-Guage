#!/usr/bin/env python3
import sqlite3 as db
from shutil import copyfile
import os
from datetime import date as label

# Author - Tim Novice sn: s3572290 RMIT
#
# Code adapted from tutorial 4 examples using 'with' keyword
# Establishes a database connection to a1data.db
# and builds data fields.
# Script should be run in the root of the directory
# where the database lives.
#
conn = db.connect('a1data.db')
dbfile = 'a1data.db'
dbfilePath = '/database/a1data.db'
if(os.path.isfile(dbfilePath)):
    bkdbfile = '/database/a1data_{}.db'.format(label.today())
    copyfile(dbfilePath, bkdbfile)
else:
    with conn:
        cursor = conn.cursor()
        try:
            cursor.execute("DROP TABLE IF EXISTS ASSIGNMENT1_data")
            cursor.execute(
                "CREATE TABLE ASSIGNMENT1_data (\
                    timestamp DATETIME, temp NUMERIC, humidity NUMERIC)")
        except db.Error as e:
            conn.log.error("Error creating Database: Cannot write to disk!" % e)
