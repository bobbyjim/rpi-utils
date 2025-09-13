#!/usr/bin/env python
import smbus
import struct
import time

def makeuint16(lsb, msb):
    return ((msb & 0xFF) << 8)  | (lsb & 0xFF)

ADDRESS                         = 0x29
VL53L0X_REG_SYSRANGE_START      = 0x000
VL53L0X_REG_RESULT_RANGE_STATUS	= 0x0014

bus = smbus.SMBus(1)

while 1:
   ret = bus.write_byte_data(ADDRESS, VL53L0X_REG_SYSRANGE_START, 0x01)
   val = bus.read_byte_data(ADDRESS, VL53L0X_REG_RESULT_RANGE_STATUS)
   data = bus.read_i2c_block_data(ADDRESS, 0x14, 12)
   DeviceRangeStatusInternal = str((data[0] & 0x78) >> 3)
   dist = str(makeuint16(data[11], data[10]))
   print( "%s : %s : %s" % ( str(val & 0x01), DeviceRangeStatusInternal, dist))
   time.sleep(0.25)
