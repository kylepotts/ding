import wiringpi2 as wp

from multiprocessing import Process,Queue
import time

from lcd import *

locations = ['Earhart', 'Ford', 'Wiley', 'Cary']
locationIndex = 0
wp.wiringPiSetup()
wp.pinMode(25,0)
wp.pinMode(24,0)
wp.pinMode(23,0)
wp.pinMode(3,0)
wp.pinMode(29,0)
wp.pinMode(28,0)

lcd = LCD()
lcd.turnOnScreen()
q = Queue()
displayState = 'location'


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
		if displayState == 'location':
			button = q.get(block=True)
			if button == "downLeft" and locationIndex > 0:
				locationIndex -=1
				lcd.writeWithSound(locations[locationIndex], "\xE4")
			if button == "upLeft" and locationIndex < len(locations)-1:
				locationIndex +=1
				lcd.writeWithSound(locations[locationIndex], "\xE4")
		time.sleep(.1)
		
			

lcd.write(locations[locationIndex])
p1 = Process(target=listenForButtons, args=(q,))
p2 = Process(target=respondToButtons, args=(q,))
p1.start()
p2.start()
while True:
	a =1 
