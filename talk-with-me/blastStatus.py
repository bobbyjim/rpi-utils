#!/usr/bin/env python
import socket
import time
import fcntl
import struct
import subprocess
import random

address = "192.168.1.255" # broadcast
port = 10203
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

def uptime():
   return subprocess.check_output('uptime')[-17:-1]

def disk():
   cmd = "df -h | awk '$NF==\"/\"{printf \"%0.1fgb %0.0f%%\", $4,$4*100/$2}'"
   return subprocess.check_output(cmd, shell = True )

def memUsage():
   cmd = "free -m | awk 'NR==2{printf \"%smb %.0f%%\", $4,$4*100/$2 }'"
   return subprocess.check_output(cmd, shell = True )

def ssid():
   try:
      SSID = subprocess.check_output('/sbin/iwgetid')[17:-2] # SSID
      line1 = SSID
   except: 
      line1 = "No SSID?"
   return line1

def ip():
   cmd = "hostname -I | cut -d\' \' -f1"
   return subprocess.check_output(cmd, shell = True )[:-1]

#           Link Quality=70/70  Signal level=-40 dBm     (from line 6)
def wifiQuality():
   cmd = "/sbin/iwconfig wlan0 | /usr/bin/perl -e '($foo) = grep(/Quality/, <>); print substr($foo,23,5)'"
   return subprocess.check_output(cmd, shell = True )

# Main Script

myip = get_ip_address("wlan0")

ip1 = ip()
up1 = uptime()
disk1 = disk()
mem1 = memUsage()
ssid1 = ssid()
q1 = wifiQuality()
q2 = q1[-2:]
q3 = q1[-5:-3]
q4 = float(q2)/float(q3)
q5 = q4
if (q4 >= 1.0):
   q5 = 0.99 
q5 = str(q5)[2:]

msg = "--- \nmsg: EHLO ph-sensor PiZero/" + myip + "\n"
msg += "name: " + subprocess.check_output('hostname')[:-1] + "\n"
msg += "date: " + time.strftime("%Y.%m.%d-%H.%M.%S") + "\n"
msg += "ip: " + ip1 + "\n"
msg += "uptime: " + up1 + "\n"
msg += "disk: " + disk1 + "\n"
msg += "mem: " + mem1 + "\n"
msg += "ssid: " + ssid1 + "\n"
msg += "quality: " + q1 + "\n"

#
#  SHORT VERSION
#
shortip = ip1[-2:]
shortup = up1[0:3]
shortdisk = disk1[-3:-1]
shortmem = mem1[-3:-1]
shortq = q1[-2:]

msg += "short: {IP: .%s, UP: %s, DF: %s, MF: %s, Q: %s}\n" % (shortip, shortup, shortdisk, shortmem, q5 );

time.sleep(5)
# print msg
sock.sendto(msg, (address, port))
