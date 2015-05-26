#!/usr/bin/env python

import os
from SETTINGS import *

logroot="/var/log/compost"
dates=[dir for dir in os.listdir(logroot)]
latestdate="140102"
for date in dates:
	if date!="errorlog":
		if int(date)>int(latestdate):
			latestdate=str(date)

sensors=[dir for dir in os.listdir(os.path.join(logroot, latestdate))]
dictionary={'sensorname':0}
for sensor in sensors:
	file=open(os.path.join(logroot,latestdate,sensor)) 	
	lastline=file.readlines()[-1].decode()
	temperature=(lastline.split(';')[-1]).rstrip()
#	if (temperature=="127.937") or (temperature=="85.000") or (temperature==".-62") or (temperature==".0"):
#		temperature="ERROR "
	dictionary[sensor]=temperature

date_of_last_measure=(lastline.split(';')[0]).rstrip()

print "\n"
print "    HEAT DISPERSION OF COMPOST HEATER IN OLGASHOF"
print "\n"
print "# -------------------------------------------------------------------------- #"
print "# The following temperature values [in Celsius] were measured at last today. #"
print "# '-' means that sensor is not reachable.                                    #"
print "# -------------------------------------------------------------------------- #"
print "\n",
print "Date of last measuring: " + str(date_of_last_measure)
print "\n",

def printTempOfSensors(temp_line_name):
	for sensor in temp_line_name:
        	if sensor in dictionary.keys():
                	temp = int(float(dictionary[sensor]))
                	print str(temp).center(7),
        	else:
                	print "-".center(7),
	print "\n" 

print "COMPOST HEATER:"
printTempOfSensors(TEMP_COMP_LINE_C)
printTempOfSensors(TEMP_COMP_LINE_B)
printTempOfSensors(TEMP_COMP_LINE_A)

if TEMP_COMP_SPIRAL_1 in sensors:
        print "SPIRAL:        " + dictionary[TEMP_COMP_SPIRAL_1].rjust(7)
if TEMP_COMP_IN in sensors:
        print "IN (cold):       " + dictionary[TEMP_COMP_IN].rjust(7)
if TEMP_COMP_OUT in sensors:
        print "OUT (hot):       " + dictionary[TEMP_COMP_OUT].rjust(7)

if TEMP_INDOOR_HIGH in sensors:
	print "INDOOR 2.5m:	" + dictionary[TEMP_INDOOR_HIGH].rjust(7)
if TEMP_INDOOR_LOW in sensors:
	print "INDOOR 1m:	" + dictionary[TEMP_INDOOR_LOW].rjust(7)
if TEMP_INDOOR_GROUND in sensors:
	print "INDOOR GROUND:	" + dictionary[TEMP_INDOOR_GROUND].rjust(7) 

print "HOT FLOWER TEMPERATURE:"
printTempOfSensors(TEMP_FLOWER_LINE_A)

print "COLD FLOWER TEMPERATURE:"
printTempOfSensors(TEMP_FLOWER_LINE_B)

if TEMP_OUTDOOR in sensors:
        print "OUTDOOR:         " + dictionary[TEMP_OUTDOOR].rjust(7)
if TEMP_OUTDOOR_GROUND in sensors:
        print "OUTDOOR GROUND:  " + dictionary[TEMP_OUTDOOR_GROUND].rjust(7)

