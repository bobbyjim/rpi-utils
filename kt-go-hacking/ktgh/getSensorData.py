#!/usr/bin/env python
import requests
import json
import sys

address = "https://ktghs.knowthings.io"

if len(sys.argv) == 1:
   print "USAGE: " + sys.argv[0] + " <sensor ID> [<gateway>]"
   print " - gateway defaults to " + address
   exit(0)

sensor = sys.argv[1]

if len(sys.argv) > 2:
   address = sys.argv[2]

# get values for a sensor
url = address + '/ktgh/dashboard/sensors/' + sensor # e.g. vl53l0x
resp = requests.get(url)
data = json.loads( resp.text )

# {"_id":"5b805d873f7dcc3fb044bf62","name":"LIDAR","ID":"vl53l0x","__v":0,"dataValue":108,"valueHistory":[{"_id":"5b8060113f7dcc3fb044bf63","dataValue":108,"timestamp":"2018-08-24T19:44:17.591Z"}]}

print "Gateway      : " + address
print "Return status: " + str(resp.status_code)
print "Sensor name  : " + data[ 'name' ]
print "Sensor ID    : " + data[ 'ID'   ]
if 'dataValue' in data:
   print "Last value   : " + str(data[ 'dataValue' ])
   print "History: "

   for item in data[ 'valueHistory' ]:
      print " - When : " + item[ 'timestamp' ]
      print "   Value: " + str(item[ 'dataValue' ])
else:
   print "No data recorded."

