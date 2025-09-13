#!/usr/bin/env python
import requests
import sys

address = "https://ktghs.knowthings.io"

if len(sys.argv) < 3:
   print "USAGE: " + sys.argv[0] + " <sensor name> <value> [<gateway>]"
   print " - gateway defaults to " + address
   exit(0)

sensor = sys.argv[1]
value  = sys.argv[2]

if len(sys.argv) > 3:
   address = sys.argv[3]

#################################################################
#
# record value for sensor
#
#################################################################
url = address + '/ktgh/requestor/sensors/' + sensor
data = '''{ "dataValue": "''' + value + '''" }'''
hdrs = { "Content-Type": "application/json" }
resp = requests.put(url, data=data, headers=hdrs)
print "Response status: " + str(resp.status_code)
