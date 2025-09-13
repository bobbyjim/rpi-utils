@echo off
rem Copyright (c) 2017 CA All rights reserved.
rem
rem Turned off the Echo above
rem Setting the required command Line arguments.
rem
set AVD_FILE_PATH=%~1
set IP_ADDRESS=%~2
set PORT_NUMER=%~3
rem
rem Run the class specified
rem
java -classpath "../lib/*"  com.ca.knowthings.AvdRunner %*
rem
rem Setting echo back on.
echo on

