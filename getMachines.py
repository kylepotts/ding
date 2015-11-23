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
	bitmap = [[0]*8]*8
	for i in range(washerLength):
		print(i)
	#print(bitmap)
		
		
			
	
	


