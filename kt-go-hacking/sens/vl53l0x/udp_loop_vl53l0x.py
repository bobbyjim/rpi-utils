#!/usr/bin/env python
import smbus
import struct
import time
import socket
import uuid
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) # for broadcast
ip   = "192.168.8.255" # for broadcast
#ip   = "192.168.8.142" # for particular machine
port = 10203


###########################################################
#
#  Set up some utils
#
###########################################################
def bswap(val):
    return struct.unpack('<H', struct.pack('>H', val))[0]
def mread_word_data(adr, reg):
    return bswap(bus.read_word_data(adr, reg))
def mwrite_word_data(adr, reg, data):
    return bus.write_word_data(adr, reg, bswap(data))
def makeuint16(lsb, msb):
    return ((msb & 0xFF) << 8)  | (lsb & 0xFF)

def VL53L0X_decode_vcsel_period(vcsel_period_reg):
# Converts the encoded VCSEL period register value into the real
# period in PLL clocks
    vcsel_period_pclks = (vcsel_period_reg + 1) << 1;
    return vcsel_period_pclks;

###########################################################
#
#  Set up some constants
#
###########################################################
VL53L0X_REG_IDENTIFICATION_MODEL_ID		= 0x00c0
VL53L0X_REG_IDENTIFICATION_REVISION_ID		= 0x00c2
VL53L0X_REG_PRE_RANGE_CONFIG_VCSEL_PERIOD	= 0x0050
VL53L0X_REG_FINAL_RANGE_CONFIG_VCSEL_PERIOD	= 0x0070
VL53L0X_REG_SYSRANGE_START			= 0x000
VL53L0X_REG_RESULT_INTERRUPT_STATUS 		= 0x0013
VL53L0X_REG_RESULT_RANGE_STATUS 		= 0x0014

###########################################################
#
#  Now the real work begins
#
###########################################################

address = 0x29           # default for VL53L0X

bus = smbus.SMBus(1)
iam = 0

while True:
   iam += 1
   try:
      val1 = bus.write_byte_data(address, VL53L0X_REG_SYSRANGE_START, 0x01)
      cnt = 0
      while (cnt < 100): # 1 second waiting time max
         time.sleep(0.01)
         val = bus.read_byte_data(address, VL53L0X_REG_RESULT_RANGE_STATUS)
         if (val & 0x01):
            break
         cnt += 1

      data = bus.read_i2c_block_data(address, 0x14, 12)
      DeviceRangeStatusInternal = ((data[0] & 0x78) >> 3)
      ready = str(val & 0x01)

      if DeviceRangeStatusInternal == 11:
         uid = str(uuid.uuid1().hex)
         siam = "%09x" % iam
         dist = str(makeuint16(data[11], data[10]))
         msg = "\n{\n   iam: %s\n   uid: %s\n   dev: vl53l0x\n   dist: %s\n}\n" % (siam, uid, dist)
         print("Sending: " + msg)
         sock.sendto(msg, (ip, port))
         time.sleep(1)
   except:
      e = sys.exc_info()
      print("Error (sensor not connected?): %s" % e)
      time.sleep(5)
