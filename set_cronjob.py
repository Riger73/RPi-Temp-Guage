#!/usr/bin/env python3

# Code adapted from week 4 PIoT code samples - RMIT 2018
# Author Tim Novice sn: s3572290 RMIT
#
# sets up application cron jobs.
# Utility script to be run once at set up while logged in as pi.
#

from crontab import CronTab


# init cron daemon
cron = CronTab(user='pi')
cron.remove_all()


# add new cron job
webserver = cron.new(command='/home/pi/WebService/display_tempdata.py &')
temp = cron.new(command='/database/temp_guage.py &')
database = cron.new(command='/database/builddb.py &')


# set job frequencies
webserver.minute.every(15)
temp.minute.every(15)
database.day.every(1)
cron.write()
