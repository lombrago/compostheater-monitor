#!/usr/bin/env python

import os, time, commands, subprocess, fcntl, logging
from SETTINGS import *

# Inicialization
logging.basicConfig(filename="compostlog.log", level=logging.DEBUG)
logheat="heat"
logimpulses="impulses"
last_imp=0
latest_imp=0
date_of_measure=str(commands.getoutput('date'))

# List of sensors of INPUT (cold) and OUTPUT (hot):
sensors=[TEMP_COMP_IN,TEMP_COMP_OUT]

# Make date directory if it does not exist
stamp=time.strftime('%y%m%d')
try:
  	os.mkdir(os.path.join(LOG_ROOT,stamp))
except OSError, e:
  	pass
log_heat_path=os.path.join(LOG_ROOT,stamp,logheat)
log_impulses_path=os.path.join(LOG_ROOT,stamp,logimpulses)

# Get starting time
starting_time=time.time()
print "Starting time: " + str(date_of_measure)
logging.debug("Starting time: " + str(date_of_measure))

# Set default GPIO states
print "Set default GPIO states."
logging.debug("Set default GPIO states.")
os.system("sudo " + HOME_DIR + "set_default_gpios.py")
os.system("sudo pkill -f " + HOME_DIR + "count_and_log_impulses.py")

# Read and log sensors
print "Read and log sensors."
logging.debug("Read and log sensors.")
os.system("sudo " + HOME_DIR + "log_rpi2_sensors.py")

# Get latest temperature of the spiral
print "Get latest temperature of the spiral."
logging.debug("Get latest temperature of the spiral.")
output=commands.getoutput("sudo " + HOME_DIR + "read_just_1_rpi2_sensor.py " + str(CH_COMP_SPIRAL) + " " + str(TEMP_COMP_SPIRAL_1))
spiral_temp=float((output.split('\n'))[-1])
print "Temperature of the spiral 1: " + str(spiral_temp) + " C." 
logging.debug("Temperature of the spiral 1: " + str(spiral_temp) + " C.")

if spiral_temp>=MIN_TEMP_OF_WATER:
	print "Water is enough hot to utilize."

	# Start counting and logging impulses from water meter
        print "Start counting and logging impulses from water meter."
        logging.debug("Start counting and logging impulses from water meter.")
        count_and_log_impulses=subprocess.Popen("sudo " + HOME_DIR + "count_and_log_impulses.py", stdout=subprocess.PIPE, shell=True)
	
	print "Pump turn ON."
	logging.debug("Pump turn ON.")
	os.popen("gpio write " + str(GPIO_PUMP_1) + " 1")
	pump=True

	# Select channel to read IN and OUT temperature values of the compost heater
	output=commands.getoutput("sudo " + HOME_DIR + "select_channel.py " + str(CH_COMP_MAIN))
	
	while pump==True:
		# Read cold and hot sensors
		runtime=time.time()
		sensor_ok=True

		print "Reading and logging temperature values measured by sensor on the selected channel."
		for sensor in sensors:
			log_file_path=os.path.join(LOG_ROOT,stamp,sensor)
			temp = commands.getoutput("owread /" + sensor + "/temperature; echo")
		  	print "ID: ", sensor, " | ", "DATE: %s |" % time.strftime('%X %x %Z'), "T: %s C " % temp
		  	if temp.startswith("ServerRead: Data error")=="True":
		    		file=open(error_log_file_path,'a')
		    		fcntl.lockf(file, fcntl.LOCK_EX)
		    		file.write("%s;%s;%s\n" % (date_of_measure, time.time(), temp))
		    		fcntl.lockf(file, fcntl.LOCK_UN)
		    		file.close()
				hot=MIN_TEMP_OF_WATER
				sensor_ok=False		
		  	if temp.startswith("ServerRead: Data error")!="True":
		    		file=open(log_file_path,'a')
		    		fcntl.lockf(file, fcntl.LOCK_EX)
		    		file.write("%s;%s;%s\n" % (date_of_measure, time.time(), temp))
		    		fcntl.lockf(file, fcntl.LOCK_UN)
		    		file.close()
		  		if sensor==TEMP_COMP_IN:
		    			cold=float(temp)
		  		if sensor==TEMP_COMP_OUT:
		    			hot=float(temp)

		os.system("sudo service owserver restart")
                time.sleep(3)

		if sensor_ok==True:
			# Get counted impulses since last read
		        file=open(log_impulses_path,'r')
		        fcntl.lockf(file, fcntl.LOCK_SH)
		        lines=file.readlines()
		        fcntl.lockf(file, fcntl.LOCK_UN)
		        file.close()
		        lastline=lines[-1]
			if "Date of measure" in lastline:
				print "Water is not flowing"
			else:
		        	latest_imp=int((lastline.split(';')[-1]).rstrip())
		       	imp=latest_imp - last_imp
			print "Counted impulses (liter of water) since last read: " + str(imp)
		       	last_imp=latest_imp
			runtime=time.time()-runtime

		        # Homennyiseg szamitasa:
		        # Q = qm x c x dT
		        # Q = homennyiseg [KJ], qm = tomegaram [Kg], c = fajho [KJ/Kg x C], dT = homerseklet kulonbseg [C]
		        # 1 liter viz = 1 kg
		        heat = (imp)*(hot-cold)*4.1813
			performance = heat/runtime
		       	print "Heat: " + str(heat) + " [KJ]"
			print "Performance: " + str(performance) + " [KW]"
#			logging.debug("Cold: " + str(cold) + " [C], Hot: " + str(hot) + " [C], Impulses: " + str(imp) + ", Heat: " + str(heat) + " [KJ], Runtime: " + str(runtime) + " [s], Performance: " + str(performance) + " [KW]")

			# Log heat to logfile
			file=open(log_heat_path, 'a')
		        fcntl.lockf(file, fcntl.LOCK_EX)
		        file.write("%s;%s;%s;%s;%s;%s;%s;%s\n" % (date_of_measure, time.time(), cold, hot, imp, heat, runtime, performance))
		        fcntl.lockf(file, fcntl.LOCK_UN)
		        file.close()

		current_time=time.time()
                duration_time=current_time-starting_time
                if duration_time>=(MAX_RUN_TIME-60):
                        print "Runtime has reached the maximum. Needs to break."
			logging.debug("Runtime has reached the maximum. Needs to break.")
                        pump=False

#		if imp==0:
#			print "Restart counting and logging impulses."
#			logging.debug("Restart counting and logging impulses.")
#			os.system("sudo pkill -f " + HOME_DIR + "count_and_log_impulses.py")
#			count_and_log_impulses=subprocess.Popen("sudo " + HOME_DIR + "count_and_log_impulses.py", stdout=subprocess.PIPE, shell=True)
#			last_imp=0
#			latest_imp=0

		if hot<(MIN_TEMP_OF_WATER-MAX_TEMP_REDUCE) and last_imp>50:
			print "Temperature of water has reduced to " + str(MIN_TEMP_OF_WATER-MAX_TEMP_REDUCE) + " celsius."
			logging.debug("Temperature of water has reduced to " + str(MIN_TEMP_OF_WATER-MAX_TEMP_REDUCE) + " celsius.")
			pump=False

#		if latest_imp>=MAX_LITER_OF_WATER:
#			print "No more hot water in heat exchanger." 
#			logging.debug("No more hot water in heat exchanger.")
#			pump=False

	print "Pump turn OFF."
	logging.debug("Pump turn OFF.")
	os.popen("gpio write " + str(GPIO_PUMP_1) + " 0")

	# Stop counting and logging impulses from water meter
	os.system("sudo pkill -f " + HOME_DIR + "count_and_log_impulses.py")
	print "Stop counting and logging impulses from water meter."
	logging.debug("Stop counting and logging impulses from water meter.")

# Set default GPIO states
print "Set default GPIO states."
os.system("sudo " + HOME_DIR + "set_default_gpios.py")

print "Running process has finished."
date_of_measure=str(commands.getoutput('date'))
logging.debug("Running process has finished." + str(date_of_measure))
