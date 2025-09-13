#!/usr/bin/env python
import requests
import json
import sys

address = "https://ktghs.knowthings.io"

if len(sys.argv) > 2:
   print "USAGE: " + sys.argv[0] + " [<gateway>]"
   print " - gateway defaults to " + address
   exit(0)

if len(sys.argv) == 2:
   address = sys.argv[1]

#######################################################################
#
# get registered sensors
#
#######################################################################
url = address + '/ktgh/dashboard/sensors'
resp = requests.get(url)
list = json.loads(resp.text)

# [{"_id":"5b805d873f7dcc3fb044bf62","name":"LIDAR","ID":"vl53l0x","__v":0,"dataValue":112,"valueHistory":[{"_id":"5b8060113f7dcc3fb044bf63","dataValue":108,"timestamp":"2018-08-24T19:44:17.591Z"},{"_id":"5b8062df3f7dcc3fb044bf64","dataValue":112,"timestamp":"2018-08-24T19:56:15.370Z"}]}]

print "Return status: " + str(resp.status_code)

for data in list:
   print " - Sensor name  : " + data[ 'name' ]
   print "   Sensor ID    : " + data[ 'ID'   ]
   if 'dataValue' in data:
      print "   Last value   : " + str(data[ 'dataValue' ])
      print "   History: "

      for item in data[ 'valueHistory' ]:
          print "    - When : " + item[ 'timestamp' ]
          print "      Value: " + str(item[ 'dataValue' ])
   else:
      print "   No data recorded."

