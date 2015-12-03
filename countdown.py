from multiprocessing import Process,Queue
from lcd import *
from sendsms import *


printToScreen = True
import time

def countdown(t,lcd,q,machineName,location):
	global printToScreen
	while t:
		if q.empty() == False:
			printToScreen = q.get()
			
		
		mins,secs = divmod(t,60)
		timeformat = machineName+ '  '+ '{:02d}:{:02d}'.format(mins,secs)+ ' at ' + location
		if printToScreen:
			lcd.write(timeformat)
		time.sleep(1)
		t-=1
	
	sendsms(machineName + ' at ' + location + ' is done ')
	lcd.write('\xD2')
	for i in range(8):
		lcd.write('\xE0')
		lcd.write('\xE3')
		lcd.write('\xE5')
	lcd.write(machineName + ' is done' + ' at ' + location)


def createCountDownProcess(t,lcd,q, machineName, location):
	p = Process(target=countdown, args=(t,lcd,q, machineName, location))
	return p
		
