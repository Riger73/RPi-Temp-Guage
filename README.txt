# RMIT 2018 semester 2
# PIoT COSC2674 (Programming the Internet of Things)
# Assignment1
# Author Timothy Novice
# Student ID: s3572290

# Utilities: to be used adhoc to perform manual tasks.
# They include the following files:
# set_cronjob.py, builddb.py, bt_builddb.py

# Core features: 3 Scripts are to be run as cron jobs and form the 
# core of the application. They include:
# temp_guage.py (The main app), managedb.py (handles the database),
# display_tempdata.py (initiates and runs the webserver), 
# alert2txt.py (cron job Pushbullet notifier),
# bt_notifier (connects to bluetooth and pushes notifications runs as a cronjob).

# The demonstration system has the database on a 58 Gigabyte partition
# Which is mounted to a directory in the root called '/database'
# This location is intentionally optional to allow for expansion. 
# However there should be a directory created mounted to the root 
# called '/database' 

# Source code structure:
|-- /
    set_cronjob.py
    temp_guage.py
    bt_notifier.py
    |-- tests
        db_tester.py
    |-- WebService/
        display_tempdata.py
        |-- templates/
            index.html
    |-- /database/
        managedb.py
        builddb.py
        bt_builddb

# Program structure: How to organise on a Raspberry Pi System
|-- /[root]
|-- /database/
    set_cronjob.py
    temp_guage.py
    managedb.py
    builddb.py
    bt_builddb
    bt_notifier
|-- /home/pi/
    |-- WebService/
        display_tempdata.py
        |-- templates/
            index.html
