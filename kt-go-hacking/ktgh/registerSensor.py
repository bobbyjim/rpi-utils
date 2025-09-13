#!/usr/bin/env python
import requests
import sys

address = "https://ktghs.knowthings.io"

if len(sys.argv) == 1:
   print "USAGE: " + sys.argv[0] + " <sensor ID> <sensor name> [<gateway>]"
   print " - gateway defaults to " + address
   exit(0)

sensor = sys.argv[1]
sensname = sys.argv[2]

if len(sys.argv) > 3:
   address = sys.argv[3]

#####################################################################
#
# register sensor
#
#####################################################################
url = address + '/ktgh/requestor/sensors'
data = '''[ { "name": "''' + sensname + '''", "ID": "''' + sensor + '''" } ]'''
hdrs = { 'Content-Type': 'application/json' }

print "debug URL = " + url
print "debug DAT = " + data

resp = requests.post(url, data=data, headers=hdrs)
print resp.status_code
