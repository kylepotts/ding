import requests
import json

API_ROOT = "http://api.tylorgarrett.com"


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

def machinesToBitmap():
    bitmap = []
    for i in range(0,8):
        r = []
        for j in range(0,8):
            r.append(0)
        bitmap.append(r)
    machinesJSONString = getMachines("shreve").encode('utf-8')
    machines = json.loads(machinesJSONString)
    machinesIndex = 0
    onDryer = True
    i = 0
    while i< 8:
        for j in range(0,8):
            machinesIndex += 1
            if(machinesIndex >= len(machines)):
                bitmap[i][j] = 0
            else:
                print(machines[machinesIndex]['type'])
                if(machines[machinesIndex]['status'] == "Available" ):
                    bitmap[i][j] = 1
                else:
                    bitmap[i][j] = 0

        i = i+1

    for row in bitmap:
        print(row)


