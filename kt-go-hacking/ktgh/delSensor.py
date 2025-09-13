#!/usr/bin/env python
import requests
import sys

address = "https://ktghs.knowthings.io"

if len(sys.argv) == 1:
   print "USAGE: " + sys.argv[0] + " <sensor ID> [<gateway>]"
   print " - gateway defaults to " + address
   exit(0)

sensor = sys.argv[1]

if len(sys.argv) > 2:
   address = sys.argv[2]

#####################################################################
#
# register sensor
#
#####################################################################
url = address + '/ktgh/dashboard/sensors/' + sensor
#data = '''[ { "name": "''' + sensname + '''", "ID": "''' + sensor + '''" } ]'''
#hdrs = { 'Content-Type': 'application/json' }

print "debug URL = " + url

resp = requests.delete(url)
print resp.status_code
