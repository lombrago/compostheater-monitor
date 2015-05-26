#!/usr/bin/env python

import os, time, commands, fcntl
from SETTINGS import *

stamp_last=time.strftime('%y%m%d')

stamp_list=[]
years=['15']
months=['01','02','03','04','05','06','07','08','09','10','11','12']
days=['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31']
for year in years:
	for month in months:
		for day in days:
			stamp=str(year)+(month)+(day)
			stamp_list.append(stamp)

for stamp in stamp_list:
        heat=0.0
        heat_sum=0.0
	performance=0.0
	performance_sum=0.0
        logpath=os.path.join(LOG_ROOT,stamp,"heat")
        if os.path.isfile(logpath):
                file=open(logpath,'r')
                fcntl.lockf(file, fcntl.LOCK_SH)
                lines=file.readlines()
                fcntl.lockf(file, fcntl.LOCK_UN)
                file.close()

                i=0
                while i<len(lines):
                        line=lines[i]
                        i+=1
                        data=(line.split(';')[-3]).rstrip()
			heat=float(data)
                        heat_sum=heat_sum+heat
#			data=(line.split(';')[-1]).rstrip()
#			performance=float(data)
#			performance_sum=performance_sum+performance

                print "Day to analyze: " + str(stamp)
                print "Summary of heat: " + str(heat_sum) + " [KJoule]"
#                print "Performance: " + str(performance) + " [KWatt]=[KJ/s]"
#                print "\n"

