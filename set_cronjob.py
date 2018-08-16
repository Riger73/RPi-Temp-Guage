#!/usr/bin/env python3

# Code taken from week 4 PIoT code samples - RMIT 2018
from crontab import CronTab
    
#init cron
cron = CronTab(user='pi')
cron.remove_all()

#add new cron job
temp  = cron.new(command='/database/temp_guage.py')
database = cron.new(command='/database/builddb.py')

#job settings
temp.minute.every(1)
database.day.every(1)
cron.write()
