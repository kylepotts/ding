from twilio.rest import TwilioRestClient
import json

account = "AC1a4978d60e81648596ecb0729fd40669"
token = "bd14b9df21940aeefa6ba1ad5062d5cf"
client = TwilioRestClient(account, token)

from_phone_num = "+13173500444"



def sendsms(message):
	print "Sending message"
	incoming = open("config.json").read();
	listOfNumbers = json.loads(incoming)
	dictionary = listOfNumbers[0];
	number = dictionary["phone_number"]
	print number
	sms = client.messages.create(body=message, to=number, from_=from_phone_num)

#sendsms("it fucking works", number)
