#!/usr/bin/env python
import socket
import time
import fcntl
import struct

ip = "192.168.8.255" # broadcast
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

myip = get_ip_address("wlan0")
msg = "--- \nmsg: EHLO ph-sensor PiZero/" + myip + "\n"
msg += "date: " + time.strftime("%Y.%m.%d-%H:%M:%S") + "\n"

sock.sendto(msg, (ip, port))

