#!/usr/bin/env python
import time
import RPi.GPIO as GPIO
import socket
import yaml

GATEWAY = "192.168.8.255" # broadcast
PORT    = 10203
sock    = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

#############################################################
#
#  Set GPIO pins
#
#############################################################
GPIO.setmode(GPIO.BCM)
GPIO_TRIGGER = 23
GPIO_ECHO    = 24
GPIO.setup(GPIO_TRIGGER,GPIO.OUT)
GPIO.setup(GPIO_ECHO,GPIO.IN)

#############################################################
#
#  Take three measurements and send one message
#
#############################################################
now = time.strftime("%Y.%m.%d-%H:%M:%S")
msg = "---\nsens:\n   hc-sr04:\n      unit: cm\n      date: %s\n" % now
metrics = []
for x in range(0,3):
   # Set trigger to False (Low)
   GPIO.output(GPIO_TRIGGER, False)
   time.sleep(0.5)
 
   # Send 10us pulse to trigger
   GPIO.output(GPIO_TRIGGER, True)
   time.sleep(0.00001)
   GPIO.output(GPIO_TRIGGER, False)
   start = time.time()
   while GPIO.input(GPIO_ECHO)==0:
     start = time.time()
 
   while GPIO.input(GPIO_ECHO)==1:
     stop = time.time()

   # Calculate pulse length
   elapsed = stop-start

   # Distance pulse travelled in that time is time
   # multiplied by the speed of sound (cm/s/2)
   dist = elapsed * 1715
   metrics.append( "%.1f" % dist )
 
msg += "      dist: [" + ", ".join(metrics) + "]\n"
sock.sendto(msg, (GATEWAY, PORT))

#############################################################
#
# Reset GPIO settings
#
#############################################################
GPIO.cleanup()
