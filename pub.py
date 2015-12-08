from pubnub import Pubnub
import json
pubnub = Pubnub(
    publish_key = "pub-c-01d2da0b-d47a-4ecf-b62d-c3a6c48bfd53",
    subscribe_key = "sub-c-af5b80e0-9d2d-11e5-a5d0-0619f8945a4f")


def onRequestPhoneNumbers(message, channel):
    with open('/home/pi/dev/ding/config.json') as data_file:
        data = json.load(data_file)
        print(data)
        pubnub.publish(channel='receive_phone_numbers', message=json.dumps(data))


def onAddNumber(message,channel):
    print(message)
    f = open('/home/pi/dev/ding/config.json', 'r')
    jsonStr = ''
    if f:
        data = json.load(f)
        data.append({'phone_number':message})
        jsonStr = json.dumps(data, indent=4, separators=(',', ': '))
    print(jsonStr)
    f.close()

    f = open('/home/pi/dev/ding/config.json', 'w+')
    if f:
        f.write(jsonStr)
    f.close()


def onRemoveNumber(message,channel):
    newData = []
    f = open('/home/pi/dev/ding/config.json', 'r')
    if f:
        data = json.load(f)
        for d in data:
            if d['phone_number'] != message:
                newData.append(d)
    f.close()
    f = open('/home/pi/dev/ding/config.json', 'w+')
    if f:
        f.write(json.dumps(newData, indent=4, separators=(',', ': ')))
    f.close()

pubnub.subscribe("get_phone_numbers", onRequestPhoneNumbers)
pubnub.subscribe("add_number", onAddNumber)
pubnub.subscribe("remove_number", onRemoveNumber)
