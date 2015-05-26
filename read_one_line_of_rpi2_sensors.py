#!/usr/bin/env python

import time, commands, os, sys
from SETTINGS import *

for arg in sys.argv:
  	i = arg

i = int(arg)
if (i < 16):
	os.system("sudo " + HOME_DIR + "select_channel.py " + str(i))

  	sensors=[]
  	owdir_output=commands.getoutput("owdir")
  	lines=owdir_output.split("\n")
  	for line in lines:
    		if line.startswith("/28."):
      			line=line[1:]
      			sensors.append(line)

  	if (sensors!=[]):
    		print "The following sensors have been found in channel " + str(i) + ":"
  	else:
    		print "No any sensor has been found in channel " + str(i) + "."

  	count=1
  	for sensor in sensors:
    		temp = commands.getoutput("owread /" + sensor + "/temperature; echo")
    		print "%2d." % count, "ID:", sensor, "|", "DATE: %s |" % time.strftime('%X %x %Z'), "T: %s C " % temp 
    		count+=1

