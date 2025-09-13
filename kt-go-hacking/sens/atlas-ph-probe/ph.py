#!/usr/bin/env python
import struct
import time     # for sleep delay and timestamps
import socket
import sys
import fcntl    # has I2C parameters like addresses


###########################################################
# 
#  Utils
#
###########################################################
def makeuint16(lsb, msb):
    return ((msb & 0xFF) << 8)  | (lsb & 0xFF)

###########################################################
#
#  Set up broadcast mode
#
###########################################################
GATEWAY = "192.168.8.255" # broadcast
PORT    = 10203
sock    = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

###########################################################
#
#  Do Your Sensor Data Collection Here
#
###########################################################
msg = "{ 'hello': 'world!' }"

address = 0x63

#
#  etc
#


###########################################################
#
# Blast packet to KnowThings Blue
#
###########################################################
sock.sendto(msg, (GATEWAY, PORT))

