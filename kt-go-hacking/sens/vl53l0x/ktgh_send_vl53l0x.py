#!/usr/bin/env python
import smbus
import struct
import time
import sys
import uuid
import requests

def makeuint16(lsb, msb):
    return ((msb & 0xFF) << 8)  | (lsb & 0xFF)

ADDRESS                         = 0x29
VL53L0X_REG_SYSRANGE_START      = 0x000
VL53L0X_REG_RESULT_RANGE_STATUS	= 0x0014

bus = smbus.SMBus(1)

url = "http://192.168.8.142:8080"

#
#  Try to register yourself
#
payload = {}
headers = { "accept": "application/json" }
r = post( url + "/sensors", payload, headers )

#
#  Send a bite of data 
#
payload = 






while True:
   iam += 1
   siam = "%09x" % iam
   uid = str(uuid.uuid1().hex)
   connection, client_address = sock.accept()
   try:
      now = time.strftime("%Y.%m.%d-%H:%M:%S")
      msg = connection.recv(40)
      print("%s  |  %s  %s  |  %s" % (now, client_address[0], client_address[1], msg))

      ret = bus.write_byte_data(ADDRESS, VL53L0X_REG_SYSRANGE_START, 0x01)
      val = bus.read_byte_data(ADDRESS, VL53L0X_REG_RESULT_RANGE_STATUS)
      data = bus.read_i2c_block_data(ADDRESS, 0x14, 12)
      DeviceRangeStatusInternal = str((data[0] & 0x78) >> 3)
      dist = str(makeuint16(data[11], data[10]))
      response = "{\n   iam: %s\n   uid: %s\n   rdy: %s\n   st: %s\n   dist: %s\n}" % (siam, uid, str(val & 0x01), DeviceRangeStatusInternal, dist)
     
      connection.sendall(response)
   except:
      connection.sendall("{ st: vl053l0x is down }")
   finally:
      connection.close() 


def post( url, payload, headers ):
   try:
      requests.post( url, data=payload, headers=headers, timeout=5.0 )
      data = handleResponse(r)
   except:
      print("POST error")

def handleResponse(response):
   print("Headers:")
   print(response.headers)
   print("Message:")
   print(response.text)
