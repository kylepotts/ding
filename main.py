import wiringpi2 as wp

from multiprocessing import Process,Queue
from getMachines import *
import time

from lcd import *

locations = ['cary', 'earhart', 'harrison', 'hawkins', 'hillenbrand','mccutheon', 'meredith_nw', 'meredith_se', 
			 'owen','shreve', 'tarkington','third','wiley','windsor_duhme','windsor_warren'];
			 

locationIndex = 0
machineIndex = 0
washers = []
dryers = []
allMachines = []
wp.wiringPiSetup()
wp.pinMode(25,0)
wp.pinMode(24,0)
wp.pinMode(23,0)
wp.pinMode(3,0)
wp.pinMode(29,0)
wp.pinMode(28,0)

lcd = LCD()
q = Queue()
displayState = 'location'
prevState = ''

def createStringFromMachine(machine):
	if machine['status'] == 'Available':
		if machine['type'] == 'Washer':
			return "%s      %s" % (machine['name'], machine['status'])
		elif machine['type'] == 'Dryer':
			return "%s       %s" % (machine['name'], machine['status'])
	
	elif machine['status'] == 'End of cycle':
		return "%s  %s" % (machine['name'], machine['status'])
		
	elif machine['status'] != 'Available':
		timeLeft = machine['time'][0:machine['time'].find('u')]
		return "%s      %s %s" % (machine['name'], machine['status'], timeLeft)
		

def listenForButtons(q):
	while True:
		if wp.digitalRead(25):
			q.put('downLeft')
		if wp.digitalRead(24):
			q.put('upLeft')
		if wp.digitalRead(23):
			q.put('select')
		if wp.digitalRead(3):
			q.put('back')
		if wp.digitalRead(29):
			q.put('downRight')
		if wp.digitalRead(28):
			q.put('upRight')
		time.sleep(.2)
	

def respondToButtons(q):
	while True:
		global locationIndex
		global locations
		global lcd
		global displayState
		global prevState
		global washers
		global dryers
		global allMachines
		button = q.get(block=True)
		#handle location
		if displayState == 'location':
			if button == "downLeft" and locationIndex > 0:
				locationIndex -=1
				lcd.write(locations[locationIndex])
				
			if button == "upLeft" and locationIndex < len(locations)-1:
				locationIndex +=1
				lcd.write(locations[locationIndex])
				
			if button == "select":
				loadingString = "Loading " + locations[locationIndex]
				prevState = "location"
				displayState = "loading"
				lcd.write(loadingString)
				machines = getMachines(locations[locationIndex])
				washers = machines[0]
				dryers = machines[1]
				for washer in washers:
					allMachines.append(washer)
				for dryer in dryers:
					allMachines.append(dryer)
					
				machineIndex = 0
				machine = allMachines[machineIndex]
				
				prevState = 'location'
				displayState = 'machines'
				lcd.write(createStringFromMachine(allMachines[machineIndex]))
				
				
		#handle loading
		elif displayState == 'loading':
			if button == 'back':
				prevState = ''
				displayState = 'location'
				locationIndex = 0
				lcd.write(locations[locationIndex])
				
		#handle machines
		elif displayState == "machines":
			if button == 'downLeft' and  machineIndex > 0:
				machineIndex-=1
				lcd.write(createStringFromMachine(allMachines[machineIndex]))
				
			elif button == 'upLeft' and machineIndex < len(allMachines)-1:
				machineIndex += 1
				lcd.write(createStringFromMachine(allMachines[machineIndex]))
				
			elif button == 'back':
				prevState = ''
				displayState = 'location'
				locationIndex = 0
				machineIndex = 0
				lcd.write(locations[locationIndex])
			
		time.sleep(.1)
		
			

lcd.write(locations[locationIndex])
p1 = Process(target=listenForButtons, args=(q,))
p2 = Process(target=respondToButtons, args=(q,))
p1.start()
p2.start()
lcd.turnOnScreen()
while True:
	a =1 
