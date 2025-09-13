#!/usr/bin/env python
import I2C_LCD_driver
import time
import subprocess
import random

# Utility functions

def show(mylcd, line1, line2, sec):
   mylcd.lcd_display_string(line1, 1)
   mylcd.lcd_display_string(line2, 2)
   time.sleep(sec)

def uptime():
   return subprocess.check_output('uptime')[-17:-1]

def disk():
   cmd = "df -h | awk '$NF==\"/\"{printf \"SD:  %0.1fgb %0.0f%%\", $4,$4*100/$2}'"
   return subprocess.check_output(cmd, shell = True )

def memUsage():
   cmd = "free -m | awk 'NR==2{printf \"Free: %smb %.0f%%\", $4,$4*100/$2 }'"
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
   return "Q: " + subprocess.check_output(cmd, shell = True )

# Main Script

mylcd = I2C_LCD_driver.lcd()

for i in (1,4):
   mylcd.lcd_clear()
   r1 = random.random()
   r2 = random.random()
   if r1 < 0.5:
      mylcd.lcd_display_string("KnowThings!", 1)
   else:
      mylcd.lcd_display_string(wifiQuality(), 1)

   if r2 < 0.5:
      mylcd.lcd_display_string(uptime(), 2)
   else:
      mylcd.lcd_display_string(memUsage(), 2)

   time.sleep(5)

mylcd.lcd_clear()
show(mylcd, ip() + " @", ssid(), 1)            # IP Address and SSID

