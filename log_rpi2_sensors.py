#!/usr/bin/env python

import os, time, commands, fcntl
from SETTINGS import *

error_log_file_path=os.path.join(LOG_ROOT,"errorlog")
stamp=time.strftime('%y%m%d')
logdir=os.path.join(LOG_ROOT,stamp)
try:
  	os.mkdir(os.path.join(LOG_ROOT,stamp))
except OSError, e:
  	pass 
date_of_measure=str(commands.getoutput('date'))

i = 0   
while (i < 16):
	os.system("sudo " + HOME_DIR + "select_channel.py " + str(i))
  	sensors=[]
  	owdir_output=commands.getoutput("owdir")
  	lines=owdir_output.split("\n")
  	for line in lines:
    		if line.startswith("/28."):
      			line=line[1:]
      			sensors.append(line)
  	count=1
  	print "Reading and logging temperature values measured by sensor on the selected channel."
	if sensors==[]:
		print "No any sensor is connected to this channel."
  	for sensor in sensors:
    		log_file_path=os.path.join(logdir,sensor)
    		old_temp=""
		temp = commands.getoutput("owread /" + sensor + "/temperature; echo")
    		print "%2d." % count, "ID:", sensor, "|", "DATE: %s |" % time.strftime('%X %x %Z'), "T: %s C " % temp 
    		if temp.startswith("ServerRead: Data error")=="True":
      			file=open(error_log_file_path,'a')
      			fcntl.lockf(file, fcntl.LOCK_EX)
      			file.write("%s;%s;%s\n" % (date_of_measure, time.time(), temp))
      			fcntl.lockf(file, fcntl.LOCK_UN)
      			file.close()
    		if os.path.exists(log_file_path):
      			file=open(log_file_path,'r')
      			fcntl.lockf(file, fcntl.LOCK_SH)
      			lines=file.readlines()
      			fcntl.lockf(file, fcntl.LOCK_UN)
      			file.close()
      			if os.path.getsize(log_file_path)>0:
        			lastline=lines[-1]
        			old_temp=(lastline.split(';')[-1]).rstrip()
    		if (old_temp != temp) and temp.startswith("ServerRead: Data error")!="True":
      			file=open(log_file_path,'a')
      			fcntl.lockf(file, fcntl.LOCK_EX)
      			file.write("%s;%s;%s\n" % (date_of_measure, time.time(), temp))
      			fcntl.lockf(file, fcntl.LOCK_UN)
      			file.close()
    		count+=1
  	i+=1
print "Done."
