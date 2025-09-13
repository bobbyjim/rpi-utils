#!/bin/sh

#  Copyright (c) 2017 CA All rights reserved.

AVD_FILE_PATH="$1"
IP_ADDRESS="$2"
PORT_NUMBER="$3"

#echo "Arguments: 1) $PCAP_FILE_PATH,  2) $IP_ADDRESS, 3) $PORT_NUMBER"

# Run the class specified
java -classpath "../lib/*"  com.ca.knowthings.AvdRunner "$@"
