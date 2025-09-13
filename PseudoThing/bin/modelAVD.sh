#!/bin/sh

#  Copyright (c) 2017 CA All rights reserved.

PCAP_FILE_PATH="$1"
IP_ADDRESS="$2"
PORT_NUMBER="$3"
ILIB_OUTPUT_FILE_PATH="$4"

#echo "Arguments: 1) $PCAP_FILE_PATH,  2) $IP_ADDRESS, 3) $PORT_NUMBER, 4) $ILIB_OUTPUT_FILE_PATH"

# Run the class specified
java -classpath "../lib/*" com.ca.knowthings.AvdModeler "$@"
