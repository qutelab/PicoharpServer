# PicoharpServer

This code provides a socket server to allow other programs to interface with a Picoharp device. This is useful if 
another program/Python script/computer cannot support the PicoQuant snAPI directly. 

One example is Qudi (Legacy version). Legacy Qudi is build on Python 3.6, however snAPI requires Python 3.12 which 
causes many dependency issues. This server is a solution allowing Qudi to send socket commands to control the Picoharp.

PicoharpServer only implements support for a very limited subset of the snAPI commands, it is intended for creating 
lifetime maps with legacy Qudi. Additional commands could be implemented for other use cases.