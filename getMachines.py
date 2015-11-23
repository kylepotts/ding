import requests
import json
import time

API_ROOT = "http://api.tylorgarrett.com"

from Adafruit_8x8 import EightByEight
grid = EightByEight(address=0x70)

def getMachines(location):
    url =  "%s/laundry/%s" % (API_ROOT,location)
    response = requests.get(url)
    response.encoding = 'utf-8'
    machines = response.json()
    
    dryers = []
    washers = []
    for machine in machines:
		if machine['type'] == 'Dryer':
			dryers.append(machine)
		elif machine['type'] == 'Washer':
			washers.append(machine)
    return [washers,dryers]

def gridPrint():
	grid.clear()
	for x in range(2, 8):
		for y in range(0, 8):
			grid.setPixel(x, y)
			time.sleep(0.05)
	time.sleep(0.5)
	grid.clear()
	time.sleep(0.5)
	
def machinesToBitMap(allMachines,washerLength, dryerLength):
	bitmap = []
	spacer = False
	for i in range(0,8):
		newRow = []
		for j in range(0,8):
			if i+j < len(allMachines):
				machine = allMachines[i+j]
				if i+j < washerLength:
					if (machine['status'] == 'Available'):
						newRow.append(1)
					else:
						newRow.append(0)
				if i+j == washerLength and spacer == False:
					print('setting')
					bitmap.append([0]*8)
					spacer = True
					
				if i+j > washerLength and i+j < washerLength+dryerLength:
					if (machine['status'] == 'Available'):
						newRow.append(1)
					else:
						newRow.append(0)
		bitmap.append(newRow)
	return bitmap
	

def printBitMap(bitmap):
	grid.clear()
	print(bitmap)
	for x in range(2, 8):
		for y in range(0, 8):
			if(bitmap[x-2][y] == 1):
				grid.setPixel(x,y)
			time.sleep(0.05)
	time.sleep(0.5)
	
	for x in range(0,2):
		for y in range(0,8):
			if(bitmap[x+4][y] == 1):
				grid.setPixel(x,y)
	
				
		
		
			
	
	


