#!/usr/bin/env python3
import sqlite3 as db
import os
from shutil import copy2
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

# Creates or overwirtes a DB with a new DB
def createDB():
    with conn:
        cursor = conn.cursor()
        try:
            cursor.execute("DROP TABLE IF EXISTS ASSIGNMENT1_data")
            cursor.execute(
                "CREATE TABLE ASSIGNMENT1_data (\
                    timestamp DATETIME, temp NUMERIC, humidity NUMERIC)")
            try:
                yield conn
            finally:
                conn.close()
        except db.Error as e:
            conn.log.error("Error creating Database: Cannot write to disk!" % e)
            conn.interrupt()


# Checks for existing db and either creates or backs up
def main():
    if(os.path.isfile(dbfilePath)):
        bkdbfile = '/database/a1data_{}.db'.format(label.today())
        copy2(dbfilePath, bkdbfile)
        if (os.path.isfile(bkdbfile)):
            createDB()
        else:
            print("New database could not be written")
    else:
        createDB()


main()