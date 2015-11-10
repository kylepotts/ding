import serial

class LCD:
	def __init__(self):
		self.display = serial.Serial("/dev/ttyAMA0", 9600, timeout=0.5)
		
	def turnOnScreen(self):
		self.display.write("\x11")
		
	def write(self, text):
		self.display.write("\x0C")
		self.display.write(text)
		
	def writeWithSound(self, text, sound):
		self.display.write("\x0C")
		self.display.write(text)
		self.display.write(sound)
		

