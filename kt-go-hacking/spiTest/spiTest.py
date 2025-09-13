import spidev
import time
import os

speeds = [10000000,20000000,25000000, 30000000, 350000000]

good_tests = []
bad_tests  = []
spi = spidev.SpiDev()
spi.open(0,0)
spi.mode = 0b01
spi.bits_per_word = 8

for a in speeds:
    
    print("Testing with SPI Clock = " + str(a))
    spi.max_speed_hz=a 
    good = 0
    bad = 0
    start = time.time()
    for i in range(100000):       
        data_byte = [0,0,0,0]            
        mask = 255
        number = i
        data_byte[0] = int(number>>0 & 255)
        data_byte[1] = int(number>>8 & 255) 
        data_byte[2] = int(number>>16 & 255)
        data_byte[3] = int(number>>24 & 255)

        spi.writebytes2([0x00, data_byte[0]]) #write to address 0
                
        spi.writebytes2([0x01])
        data_in = spi.readbytes(1)
                       
        if data_in[0] == data_byte[0]:
            good = good + 1
        else:
            bad = bad + 1

    stop = time.time()
    time.sleep(0.05)
    print(stop - start)

    print(good)
    print(bad)
