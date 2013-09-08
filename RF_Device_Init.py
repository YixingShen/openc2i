#!/usr/bin/env python

import sys
import os
import serial

class RF_Device_Init (object):

	def init_device (self, _port, _baudrate, _bytesize, _parity, _stopbits, _timeout, _xonoff, _rtscts, _dsrdtr):
		dev = serial.Serial()
		dev.port = _port
		dev.baudrate = _baudrate
		dev.bytesize = _bytesize
		dev.parity = _parity
		dev.stopbits = _stopbits
		dev.timeout = _timeout
		dev.xonoff = _xonoff
		dev.rtscts = _rtscts
		dev.dsrdtr = _dsrdtr
		return dev


