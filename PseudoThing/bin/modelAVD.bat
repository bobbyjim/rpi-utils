@echo off
rem Copyright (c) 2017 CA All rights reserved.
rem
rem Turned off the Echo above
rem Setting the required command Line arguments.
rem
set PCAP_FILE_PATH=%~1
set IP_ADDRESS=%~2
set PORT_NUMBER=%~3
set ILIB_OUTPUT_FILE_PATH=%~4
rem
rem Run the class specified
rem
java -classpath "../lib/*" com.ca.knowthings.AvdModeler %*
rem
rem Setting echo back on.
echo on