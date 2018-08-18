#!/usr/bin/env python3
import sqlite3 as db

conn = db.connect('a1data.db')
with conn:
    curs = conn.cursor()
    curs.execute("DROP TABLE IF EXISTS ASSIGNMENT1_data")
    curs.execute(
        "CREATE TABLE ASSIGNMENT1_data(timestamp DATETIME, temp NUMERIC, humidity NUMERIC)")
        
