# PseudoThing 

PseudoThing is KnowThings.io’s pre-release prototype bringing our fancy math algorithms to IoT. We are working on making devices that you can use to build your software before physical devices are ready, test your software at scale, and predict the interactions of real devices before field testing. 

# Known Platforms

Theoretically, PseudoThing should work on any platform with Java 8. We’ve currently tested: 

       Linux
       Mac
       Raspbian
       Windows 8 and Windows 10


# Prerequisites

Oracle or Open JDK 8.



# Install

Ensure there is a JDK on the system and that java is in the filepath.
Unzip the PseudoThing.zip into a directory and you are done.

# Use

PseudoThing creates a simulation using a 3 step process.  

1) Capture

2) Model

3) Playback

## Step 1 -- Capture
Generate a PCAP file with the transactions that you want (we use wireshark). You don’t have to filter out other traffic, but you can if you want to (we do to isolate device traffic).  If using wireshark, make sure you save your capture as a PCAP file as that is the only format we support.  However, using Wireshark you can open a pcapng or other capture file and save as a .pcap and it should work.  We are exploring a known issue with TShark at this time.

## Step 2 -- Model
The fun part! Here you will create your first AVD (adaptive virtual device)
Create your PseudoThing by running this command:

Unix, Linux or Mac:
```
modelAVD.sh
```

Windows Operatings Sytems:

```
modelAVD.bat
```

Run the command in the bin directory inside the PseudoThing directory. If you want to run it anywhere else, set the classpath.

modelAVD.sh takes the following parameters:

```
modelAVD.sh <path to pcap file> <server IP address> <Server Listening Port> <AVD Name - optional>
```

### Parameter Terms
Path to PCAP file:  The absolute or relative path to the .pcap file that contains the transactions to be modeled.

Server IP Address:  This is the server or gateway that the device is communicating with.  Currently PseudoThing supports devices which initiate connections.  We filter out communications based on the where your device is sending data.

Server Listening Port:  The port which you server is listening on for device messages.

AVD Name:  The name for the model you are creating.  This is just a descriptive name. Files will be created using this name, so only use characters that are valid for your operating systems file names.  If you do not supply a name, one will be created with a prefix AVD followed by an integer, for the number of AVD’s that have been created.


### Arguments
modelAVD supports the following arguements:

       -h, --help
              Displays this help text.
       -f <PCAP file>, --pcapFile=<PCAP file>
              Specifies the path of the pcap file to create a model from.
       -a <AVD Name>, --avdName=<AVD Name>
              Name of the model, referred as adaptive virtual device (AVD). 
              [OPTIONAL]
       -i <Server IP Address>, --ip=<Server IP Address>
              IP Address of system under test (SUT)
       -p <Server Port>, --port=<Server Port>
              Port number of the system under test (SUT)
              

### Examples

```
./modelAVD.sh /home/knowthings/myPcap.pcap 10.10.10.1 2048 MyFirstAVD
```

```
modelAVD.bat -f C:\Users\MyIoT\PseudoThing\bin\exampleLocal.pcap -a MyFirstAVD -i 192.168.0.0 -p 63473
```

```
modelAVD.bat --pcapFile=exampleLocal.pcap --avdName=MyFirstAVD --ip=172.16.0.0 --port=63473
```



## Step 3 Playback
Once you have your PseudoThing AVD model, you can play it back and have it stand in for the device you recorded.  

On Mac, Linux, and Linux Operating Systems use:

```
runAVD.sh
```

On Windows Operating Systems:

```
runAVD.bat
```

It also must be run from the bin directory of your PseudoThing directory.

runAVD.sh takes the following parameters:

```
runAVD.sh <AVD name> <Server IP Address> <Server Port>
```

### Parameter Terms

AVD Name: The name of the AVD you used in step 2.

Server IP Address:  The IP address where your virtual device will send messages.  This is likely the same address you used in Step 2.

Server Port:  The port your server is listening on for device messages.  This is likely the same port you used in Step 2.

### Arguments

runAVD supports the following arguments:

       -h, --help
              Displays this help text.
       -a <AVD Name>, --avdName=<AVD Name>
              Name of the AVD to playback
       -i <Server IP Address>, --ip=<Server IP Address>
              IP Address of system under test (SUT)
       -p <Server Port>, --port=<Server Port>
              Port number of the SUT to which this AVD would connect
       -r, --responder
              Run this AVD as Responder. SUT IP and Port are NOT REQUIRED for 
              this mode.
       -s <Responder Port>, --respPort=<Responder Port>
              Port number at which the AVD responder would run, and "serve" 
              the responses from. Only USED if running as responder, but is 
              OPTIONAL. If not provided, the DEFAULT port used is 8111
### Examples

```
./runAVD.sh MyFirstAVD 10.10.10.1 2048 
```
```
C:\Users\MyIoT\PseudoThing\bin>runAVD.bat -a MyTestAVD -i 172.16.0.0 -p 63473

```
```
C:\Users\MyIoT\PseudoThing\bin>runAVD.bat --avdName=MyTestAVD --ip=192.168.0.0 --port=63473
```

# Run AVD as a Requestor Client Device
A requestor device is a device that initiates contact with the software. It is awake and keeps a port open while it is requesting information and getting a response back.

To run the AVD as a requester/client device:
```
   runAVD.sh -a <AVD name> -i <Server IP Address> -p <Server Port>
   runAVD.sh --avdName=<AVD name> --ip=<Server IP Address> --port=<Server Port>
```

# Run AVD as a Responder Client Device
A responder client device is a device that respondes to a request from software. It is alseep and awakens when it is pinged.

To run the AVD as a responder device:

 ```
   runAVD.sh -a <AVD name> -r -s <Responder Port>
   runAVD.sh --avdName=<AVD name> --responder --respPort=<Responder Port>
 ```
