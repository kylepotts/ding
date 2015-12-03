from multiprocessing import Process,Queue
from lcd import *


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
	
	lcd.write('\xD8')
	for i in range(8):
		lcd.write('\xD3')
		lcd.write('\xE4')
		lcd.write('\XDC')
		lcd.write('\xD4')
		lcd.write('\xDE')
	lcd.write(machineName + ' is done' + ' at ' + location)


def createCountDownProcess(t,lcd,q, machineName, location):
	p = Process(target=countdown, args=(t,lcd,q, machineName, location))
	return p
		
