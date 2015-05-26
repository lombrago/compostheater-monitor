#!/usr/bin/env python

import os, time, commands, fcntl
import RPi.GPIO as GPIO
from SETTINGS import *


# A program megszamolja, hogy hany darab impulzus erkezik a megadott bemenetre.
# A bemenet a megadott GPIO_IMP szammal azonosithato.
# Keszitette: ebaltgy

# Set input for counting interrupts
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_COUNTER_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Initialization
logfilename="impulses"
count=0
counting=True
date_of_measure=str(commands.getoutput('date'))

# Make date directory if it does not exist
stamp=time.strftime('%y%m%d')
try:
  	os.mkdir(os.path.join(LOG_ROOT,stamp))
except OSError, e:
  	pass

# Set log file
log_file_path=os.path.join(LOG_ROOT,stamp,logfilename)

# Log the date of measure in the logfile 
print "Date of measure: " + str(date_of_measure)
file=open(log_file_path,'a')
fcntl.lockf(file, fcntl.LOCK_EX)
file.write("%s%s\n" % ("Date of measure: ", date_of_measure))
fcntl.lockf(file, fcntl.LOCK_UN)
file.close()

# Count and log the summary number of impulses in the logfile
while counting==True:
	GPIO.wait_for_edge(GPIO_COUNTER_1, GPIO.FALLING)
	GPIO.wait_for_edge(GPIO_COUNTER_1, GPIO.RISING)
	count+=1
	print str(count)
        file=open(log_file_path,'a')
        fcntl.lockf(file, fcntl.LOCK_EX)
        file.write("%s;%s\n" % (time.time(), count))
        fcntl.lockf(file, fcntl.LOCK_UN)
        file.close()

