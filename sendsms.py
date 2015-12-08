from twilio.rest import TwilioRestClient
import json

account = "AC1a4978d60e81648596ecb0729fd40669"
token = "bd14b9df21940aeefa6ba1ad5062d5cf"
client = TwilioRestClient(account, token)



def sendsms(message):
	print "Sending message"
	incoming = open("config.json").read();
	listOfNumbers = json.loads(incoming)

	for n in listOfNumbers:
		print('sending message to ' + n['phone_number'])
		number = n['phone_number']
		sms = client.messages.create(body=message, to=number, from_=from_phone_num)
