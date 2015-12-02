from twilio.rest import TwilioRestClient

account = "AC1a4978d60e81648596ecb0729fd40669"
token = "bd14b9df21940aeefa6ba1ad5062d5cf"
client = TwilioRestClient(account, token)

from_phone_num = "+13173500444"


def sendsms(message, to):
	print "Sending message"
	sms = client.messages.create(body=message, to=to, from_=from_phone_num)

sendsms("This is the message", "3174903924")