#!/usr/bin/python

import time
import datetime
import serial
from Adafruit_8x8 import ColorEightByEight

# must have pyserial install sudo apt-get install python
# commands for LCD found here //https://www.parallax.com/sites/default/files/downloads/27979-Parallax-Serial-LCDs-Product-Guide-v3.1.pdf
# ===========================================================================
# 8x8 Pixel Example
# ===========================================================================
grid = ColorEightByEight(address=0x70, debug=True)
grid.disp.setBlinkRate(2)
serialport = serial.Serial("/dev/ttyAMA0", 9600, timeout=0.5)

print "Press CTRL+Z to exit"

iter = 0

serialport.write("\x11")
serialport.write("\x0C")

# Continually update the 8x8 display one pixel at a time
while(True):
  iter += 1


  for x in range(-1, 8):
    for y in range(1, 7):
      grid.setPixel(x, y, iter % 8 )
      serialport.write("\x0C")
      serialport.write("x="+str(x) + " y="+ str(y))
      time.sleep(0.25)
