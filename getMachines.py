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
	
	
def machinesToBitMap(allMachines, washerLength, dryerLength):
	index = 0
	bitmap = []
	row = []
	leftToFill = 0
	while(index <= 64):
		if (len(row) == 8 and index!= 0):
			bitmap.append(row)
			row = []
			
		if ((index-leftToFill < washerLength) or (index-leftToFill > washerLength and index-leftToFill < len(allMachines))):
			machine = allMachines[index-leftToFill]
			if machine['status'] == 'Available':
				row.append(1)
			else:
				row.append(0)
				
			
		elif index == washerLength:
			leftToFill = (index%8)
			print(leftToFill)
			for n in range(0,8-leftToFill):
				row.append(0)
			bitmap.append(row)
			row = []
			
			bitmap.append([1,0,0,1,0,0,0,1])
			index = index+leftToFill
			
		else:
			row.append(0)
		index = index+1
	return bitmap
	

def printBitMap(bitmap):
	grid.clear()
	for x in range(2, 8):
		for y in range(0, len(bitmap[x-2])):
			if(bitmap[x-2][y] == 1):
				grid.setPixel(x,y)
				
	
	for y in range(0,8):
		if(bitmap[5][y] == 1):
			grid.setPixel(7,y)
			
	for y in range(0,8):
		if(bitmap[6][y] == 1):
			grid.setPixel(0,y)
			
	for y in range(0,8):
		if (bitmap[7][y] == 1):
			grid.setPixel(1,y)
		

def clearGrid():
	grid.clear()
	
				
		
		
			
	
	


