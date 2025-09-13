#!/usr/bin/env python
import socket
import time
import yaml

port = 10203
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', port))


iph = ''
up = ''
mem = ''
disk = ''
q = ''

count = 0
while count < 3:
   (msg, address) = sock.recvfrom(4096)
   # print msg
   obj = yaml.load(msg)
   s = obj['short']
   # print(s)
   iph += str(s['IP'])[1:] + ' '
   up  += str(s['UP']) + ' '
   mem += str(s['MF']) + '% '
   disk += str(s['DF']) + '% '
   q    += str(s['Q'])[0:3] + '% '
   count += 1

print "--- "
print "time: " + time.strftime("%a, %d %b %Y %H:%M")
print "IP: " + iph
print "UP: " + up
print "MF: " + mem
print "DF: " + disk
print "Q : "  + q
