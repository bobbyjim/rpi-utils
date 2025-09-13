#!/usr/bin/env python
import requests
import sys

address = "https://ktghs.knowthings.io"

if len(sys.argv) == 1:
   print "USAGE: " + sys.argv[0] + " <actuator ID> [<gateway>]"
   print " - gateway defaults to " + address
   exit(0)

actuator = sys.argv[1]

if len(sys.argv) > 2:
   address = sys.argv[2]

#####################################################################
#
# register sensor
#
#####################################################################
url = address + '/ktgh/dashboard/actuators/' + actuator

#print "debug URL = " + url

resp = requests.delete(url)
print resp.status_code
