#!/usr/bin/env python3
import sqlite3 as db

# Author Tim Novice sn: s3572290 RMIT
#
# Tests data is saving to the database by displaying database content
#

tempds = '/database/a1data.db'

def displayData():
    conn = db.connect(tempds)
    curs = conn.cursor()
    print("\nDatabase contents:\n")
    for row in curs.execute("SELECT * FROM ASSIGNMENT1_data;"):
        print(row)
    conn.close()
