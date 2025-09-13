#!/usr/bin/env python
import smbus
import struct
import time
import socket
import sys



MODE = 'BASIC'

if len(sys.argv) > 1:
   MODE = str(sys.argv[1])



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

model   = bus.read_byte_data(address, VL53L0X_REG_IDENTIFICATION_MODEL_ID)
revision = bus.read_byte_data(address, VL53L0X_REG_IDENTIFICATION_REVISION_ID)

################################################################################
#
#	case VL53L0X_VCSEL_PERIOD_PRE_RANGE:
#		Status = VL53L0X_RdByte(Dev,
#			VL53L0X_REG_PRE_RANGE_CONFIG_VCSEL_PERIOD,
#			&vcsel_period_reg);
#
################################################################################
prerange = bus.read_byte_data(address, VL53L0X_REG_PRE_RANGE_CONFIG_VCSEL_PERIOD)


################################################################################
#
#	case VL53L0X_VCSEL_PERIOD_FINAL_RANGE:
#		Status = VL53L0X_RdByte(Dev,
#			VL53L0X_REG_FINAL_RANGE_CONFIG_VCSEL_PERIOD,
#			&vcsel_period_reg);
#
################################################################################
finalrange = bus.read_byte_data(address, VL53L0X_REG_FINAL_RANGE_CONFIG_VCSEL_PERIOD)

#		Status = VL53L0X_WrByte(Dev, VL53L0X_REG_SYSRANGE_START, 0x01);
val1 = bus.write_byte_data(address, VL53L0X_REG_SYSRANGE_START, 0x01)

################################################################################
#
#		Status = VL53L0X_RdByte(Dev, VL53L0X_REG_RESULT_RANGE_STATUS,
#			&SysRangeStatusRegister);
#		if (Status == VL53L0X_ERROR_NONE) {
#			if (SysRangeStatusRegister & 0x01)
#				*pMeasurementDataReady = 1;
#			else
#				*pMeasurementDataReady = 0;
#		}
#
################################################################################
cnt = 0
while (cnt < 100): # 1 second waiting time max
	time.sleep(0.010)
	val = bus.read_byte_data(address, VL53L0X_REG_RESULT_RANGE_STATUS)
	if (val & 0x01):
		break
	cnt += 1


status = val & 0x01

#	Status = VL53L0X_ReadMulti(Dev, 0x14, localBuffer, 12);
data = bus.read_i2c_block_data(address, 0x14, 12)

DeviceRangeStatusInternal = ((data[0] & 0x78) >> 3)
rangeFound = (DeviceRangeStatusInternal == 11)

now = time.strftime("%Y.%m.%d-%H:%M:%S")

distance = str(makeuint16(data[11], data[10]))


msg = "--- # VL53L0X:%s %s\n" % ( hex(address), now )

if MODE == 'BASIC':
   msg += "dist: %s\n" % distance
else:
   msg += "sens:\n"
   msg += "  vl53l0x:\n"
   msg += "    addr: %s\n" % hex(address)
   msg += "    hardware:\n"
   msg += "      model: %s\n" % hex(model)
   msg += "      revision: %s\n" % hex(revision)
   msg += "      PRE_RANGE_CONFIG_VCSEL_PERIOD: { value: %s, decoded: %s }\n" % (hex(prerange), str(VL53L0X_decode_vcsel_period(prerange)))
   msg += "      FINAL_RANGE_CONFIG_VCSEL_PERIOD: { value: %s, decoded: %s }\n" % (hex(finalrange), str(VL53L0X_decode_vcsel_period(finalrange)))
   msg += "    raw: %s\n" % data
#   msg += "    status: %s\n" % status
   msg += "    internal status: %s\n" % DeviceRangeStatusInternal
   msg += "    ambient count: %s\n" % str(makeuint16(data[7], data[6]))
   msg += "    signal count: %s\n" % str(makeuint16(data[9], data[8]))
   msg += "    dist: %s\n" % distance

#msg += "...\n";

send = (rangeFound == 1)

if send:
   sock.sendto(msg, (GATEWAY, PORT))

