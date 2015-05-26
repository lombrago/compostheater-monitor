#!/usr/bin/env python

import time, commands, os, sys
from SETTINGS import *

for arg in sys.argv:
	i = arg

i = int(arg) 
if (i < 16): 
	A=(i%2)
  	B=((i/2)%2)
  	C=((i/4)%2)
  	D=(i/8)
  	os.system("gpio write " + str(GPIO_MULTIPLEXER_0) + " " + str(A))
  	os.system("gpio write " + str(GPIO_MULTIPLEXER_1) + " " + str(B))
  	os.system("gpio write " + str(GPIO_MULTIPLEXER_2) + " " + str(C))
  	os.system("gpio write " + str(GPIO_MULTIPLEXER_3) + " " + str(D))
  	print "Channel " + str(i) + " (ABCD=" + str(A) + str(B) + str(C) + str(D) + ") is selected in multiplexer."
  	print "Refreshing list of sensors on the selected channel."
#	time.sleep(3)
  	os.system("sudo service owserver restart")
#	time.sleep(3)

else:
	print "Error: Invalid parameter. Use integer from 0 to 15 as argument!"

