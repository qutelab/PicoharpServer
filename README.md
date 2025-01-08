# PicoharpServer

This code provides a socket server to allow other programs to interface with a Picoharp device. This is useful if 
another program/Python script/computer cannot support the PicoQuant snAPI directly. 

One example is Qudi (Legacy version). Legacy Qudi is build on Python 3.6, however snAPI requires Python 3.12 which 
causes many dependency issues. This server is a solution allowing Qudi to send socket commands to control the Picoharp.

PicoharpServer only implements support for a very limited subset of the snAPI commands, it is intended for creating 
lifetime maps with legacy Qudi. Additional commands could be implemented for other use cases.

Picoharp settings are adjusted in the `.ini` file in `/PicoharpConfig/`. Example:
```
[Device]
HystCode = 0
SyncDiv = 1
SyncTrigMode = 0
SyncEdgeTrig = -250,0
SyncChannelOffset = 0
SyncChannelEnable = 1
SyncDeadTime = 0
StopCount = 1000
Binning = 1
Offset = 0
TriggerOutput = 0

[All_Channels]
TrigMode = 0
ChanOffs = 0
ChanEna = 1
DeadTime = 0
EdgeTrig = 450,0
```

Note: Histogram time is hardcoded in `PicoharpServer.py`. There is also a `system.ini` config file in the snAPI library that contains some settings.
