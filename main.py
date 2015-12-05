import wiringpi2 as wp

from multiprocessing import Process,Queue
from getMachines import *
from countdown import *
import time

from lcd import *

locations = ['cary', 'demo', 'harrison', 'hawkins', 'hillenbrand','mccutheon', 'meredith_nw', 'meredith_se', 
			 'owen','shreve', 'tarkington','third','wiley','windsor_duhme','windsor_warren'];
			 

locationIndex = 0
machineIndex = 0
washers = []
dryers = []
allMachines = []
countDownProcess = None
wp.wiringPiSetup()
wp.pinMode(25,0)
wp.pinMode(24,0)
wp.pinMode(23,0)
wp.pinMode(3,0)
wp.pinMode(29,0)
wp.pinMode(28,0)

lcd = LCD()
q = Queue()
countQueue = Queue()
displayState = 'location'
prevState = ''

def createStringFromMachine(machine):
	if machine['status'] == 'Available':
		if machine['type'] == 'Washer':
			s = "%s  %s" % (machine['name'],machine['status'])
			return splitForLCD(s)
			
		elif machine['type'] == 'Dryer':
			s = "%s  %s" % (machine['name'], machine['status'])
			return splitForLCD(s)
			
	
	elif machine['status'] == 'End of cycle':
		s = "%s  %s" % (machine['name'], machine['status'])
		return splitForLCD(s)
		
	elif machine['status'] != 'Available':
		timeLeft = machine['time'][0:machine['time'].find('u')]
		s = "%s  %s %s" % (machine['name'], machine['status'], timeLeft)
		return splitForLCD(s)
		

def splitForLCD(s):
	charWritten = 0
	newString = []
	words = s.split()
	for word in words:
		if len(word)+charWritten <= 16:
			for char in word:
				newString.append(char)
				charWritten += 1
		else:
			left = 16 - charWritten
			for i in range(0,left):
				newString.append(' ')
				charWritten += 1
			charWritten = 0
			
			if len(word) > 16:
				print('fix')
			else:
				for char in word:
					newString.append(char)
					charWritten += 1
			
		newString.append(' ')
		charWritten += 1
			
	s = ''.join(newString)[0:32]
	return s[0:32] 
		

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
		global countQueue
		global countDownProcess
		button = q.get(block=True)
		
		if countDownProcess != None and countDownProcess.is_alive() == False:
			countDownProcess = None
		
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
				time.sleep(.1)
				printBitMap(machinesToBitMap(allMachines,len(washers), len(dryers)))
				
				
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
				allMachines = []
				lcd.write(locations[locationIndex])
				clearGrid()
			
			elif button == 'select':
				prevState = 'machines'
				displayState = 'timer'
				t = allMachines[machineIndex]['time']
				t= t.replace(u'\xa0',u'')
				if t  == u'':
					lcd.write('Machine         is available')
					time.sleep(0.75)
					lcd.write(createStringFromMachine(allMachines[machineIndex]))
					displayState = 'machines'
				else:
					t = [int(s) for s in allMachines[machineIndex]['time'].split() if s.isdigit()]
					timeInSeconds = t[0]*60
					countDownProcess = createCountDownProcess(timeInSeconds,lcd,countQueue, allMachines[machineIndex]['name'], locations[locationIndex])
					countDownProcess.start()
					
			
		
		elif displayState == 'timer':
			
			if button == 'back':
				prevState = displayState
				displayState = 'location'
				locationIndex = 0
				lcd.write(locations[locationIndex])
				grid.clear()
				countQueue.put(False)
				
		if button == 'upRight':
			
			if countDownProcess != None:
				lcd.clear()
				prevState = displayState
				displayState = 'timer'
				countQueue.put(True)
			else:
				print('Process is none')
				
		if button == 'downRight':
			if countDownProcess != None:
				if displayState == 'timer':
					if prevState == 'machines':
						prevState = 'timer'
						displayState = 'machines'
						lcd.write(createStringFromMachine(allMachines[machineIndex]))
					elif prevState == 'location':
						prevState = 'timer'
						displayState = 'location'
						lcd.write(locations[locationIndex])
				
				countDownProcess.terminate()
			
		time.sleep(.1)
		
			

lcd.write(locations[locationIndex])
p1 = Process(target=listenForButtons, args=(q,))
p2 = Process(target=respondToButtons, args=(q,))
p1.start()
p2.start()
lcd.turnOnScreen()
while True:
	a =1 
