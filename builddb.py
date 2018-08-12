import sqlite3

conn = sqlite3.connect('a1data.db')
with conn:
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS ASSIGNMENT1_data")
    cursor.execute(
        "CREATE TABLE ASSIGNMENT1_data (timestamp DATETIME, temp NUMERIC, humidity NUMERIC)")
        
