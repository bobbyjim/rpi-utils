#!/usr/bin/env python
import smbus
import struct
import time
import socket
import sys
import uuid

def makeuint16(lsb, msb):
    return ((msb & 0xFF) << 8)  | (lsb & 0xFF)

ADDRESS                         = 0x29
VL53L0X_REG_SYSRANGE_START      = 0x000
VL53L0X_REG_RESULT_RANGE_STATUS	= 0x0014

bus = smbus.SMBus(1)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('',10203))

sock.listen(1)
iam = 0

while True:
   iam += 1
   siam = "%09x" % iam
   uid = str(uuid.uuid1().hex)
   connection, client_address = sock.accept()
   try:
      now = time.strftime("%Y.%m.%d-%H:%M:%S")
      msg = connection.recv(40)
      ret = bus.write_byte_data(ADDRESS, VL53L0X_REG_SYSRANGE_START, 0x01)
      val = bus.read_byte_data(ADDRESS, VL53L0X_REG_RESULT_RANGE_STATUS)
      data = bus.read_i2c_block_data(ADDRESS, 0x14, 12)
      DeviceRangeStatusInternal = str((data[0] & 0x78) >> 3)
      dist = str(makeuint16(data[11], data[10]))
      print("%s  |  %s  %s  |  %s  | %s" % (now, client_address[0], client_address[1], msg, dist))
      response = "{\n   iam: %s\n   uid: %s\n   rdy: %s\n   st: %s\n   dist: %s\n}" % (siam, uid, str(val & 0x01), DeviceRangeStatusInternal, dist)
     
      connection.sendall(response)
   except:
      connection.sendall("{ st: vl053l0x is down }")
   finally:
      connection.close() 

