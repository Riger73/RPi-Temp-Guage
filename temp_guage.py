from sense_hat import SenseHat
from datetime import datetime
from threading import Timer
# Author Tim Novice sn: s3572290 RMIT
#
# Gathers temerature and offsets from device heat.
# Returns calibrated temerature and date time
# Cycles through periodically until receiving exit feed
# To be used as a cron task.
#
sense = SenseHat()
sense.clear()

def polltemp():    
    temp = sense.get_temperature()
    sense.show_message(
        'Temp: {0:0.1f} *c'.format(temp), scroll_speed = 0.05)
    sense.clear()
    date_time = datetime.now().strftime("%H:%M")

# Timer thread for temperature poll that polls evey 5 milliseconds
t = Timer(0.5, polltemp)
t.start()
