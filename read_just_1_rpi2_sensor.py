#!/usr/bin/env python

import time, commands, os, sys
from SETTINGS import *

i=int(sys.argv[1])
sensor_id=str(sys.argv[2])

if (i<16):
	os.system("sudo " + HOME_DIR + "select_channel.py " + str(i))
  	sensors=[]
  	owdir_output=commands.getoutput("owdir")
  	lines=owdir_output.split("\n")
  	for line in lines:
    		if line.startswith("/28."):
      			line=line[1:]
      			sensors.append(line)

  	if (sensors!=[]):
    		for sensor in sensors:
      			if sensor==sensor_id:
 	       			print "ID: " + sensor
        			temp = commands.getoutput("owread /" + sensor + "/temperature; echo")
        			print temp

