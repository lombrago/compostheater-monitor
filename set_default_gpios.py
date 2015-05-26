#!/usr/bin/env python

import os
from SETTINGS import *

print "Stop counting and logging of impulses"
os.system("sudo pkill -9 -f " + HOME_DIR + "count_and_log_impulses.py")

# Set input to count pulses comming from the water meter
print "Set input to count pulses comming from the water meter: GPIO_COUNTER_1 = " + str(GPIO_COUNTER_1)
os.system("gpio mode " + str(GPIO_COUNTER_1) + " in")

# Set output to switch on/off the pump
print "Set output to switch on/off the pump: GPIO_PUMP_1 = " + str(GPIO_PUMP_1)
os.system("gpio mode " + str(GPIO_PUMP_1) + " out")
os.system("gpio write " + str(GPIO_PUMP_1) + " 0")

# Set output to select temperature meter lines in multiplexer
print "Set output to select temperature meter lines in multiplexer: GPIO_MULTIPLEXER_0 = " + str(GPIO_MULTIPLEXER_0)
print "Set output to select temperature meter lines in multiplexer: GPIO_MULTIPLEXER_1 = " + str(GPIO_MULTIPLEXER_1)
print "Set output to select temperature meter lines in multiplexer: GPIO_MULTIPLEXER_2 = " + str(GPIO_MULTIPLEXER_2)
print "Set output to select temperature meter lines in multiplexer: GPIO_MULTIPLEXER_3 = " + str(GPIO_MULTIPLEXER_3)
os.system("gpio mode " + str(GPIO_MULTIPLEXER_0) + " out")
os.system("gpio mode " + str(GPIO_MULTIPLEXER_1) + " out")
os.system("gpio mode " + str(GPIO_MULTIPLEXER_2) + " out")
os.system("gpio mode " + str(GPIO_MULTIPLEXER_3) + " out")
os.system("gpio write " + str(GPIO_MULTIPLEXER_0) + " 0")
os.system("gpio write " + str(GPIO_MULTIPLEXER_1) + " 0")
os.system("gpio write " + str(GPIO_MULTIPLEXER_2) + " 0")
os.system("gpio write " + str(GPIO_MULTIPLEXER_3) + " 0")

