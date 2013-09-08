#!/usr/bin/env python

import serial
from ConfigParser import RawConfigParser
from RF_Device_Init import *

class RF_Sys_Init (object):
	version = 0.2
	RF_Serial_Conf = "/etc/RF_Serial/config"
	_port = None
	_baudrate = None
	_bytesize = None
	_parity = None
	_stopbits = None
	_timeout = None
	_xonxoff = None
	_rtscts = None
	_dsrdtr = None
	_modem_mac = None
	_c2i_server_ip = None
	_c2i_server_port = None
	rcp = None
	_field_separator = ":"
	SUCCESS = 0
	ERROR = 1
	device = None


	def config_parser(self):
		rcp = RawConfigParser()
		if rcp.read(self.RF_Serial_Conf) == []:
			return self.ERROR
		"""[Serial port parameters]"""
		self._port = rcp.get("PORT_CONFIG","port").strip("")
		self._baudrate = rcp.get("PORT_CONFIG","baudrate").strip("")
		self._bytesize = rcp.get("PORT_CONFIG","bytesize").strip("")
		self._parity = rcp.get("PORT_CONFIG","parity").strip("")
		self._stopbits = rcp.get("PORT_CONFIG","stopbits").strip("")
		self._timeout = rcp.get("PORT_CONFIG","timeout").strip("")
		self._xonxoff = rcp.get("PORT_CONFIG","xonxoff").strip("")
		self._rtscts = rcp.get("PORT_CONFIG","rtscts").strip("")
		self._dsrdtr = rcp.get("PORT_CONFIG","dsrdtr").strip("")
		self._modem_mac = rcp.get("PORT_CONFIG","modem_mac").strip("")
		self._c2i_server_ip = rcp.get("C2I_CONFIG","server_ip").strip("")
		self._c2i_server_port = rcp.get("C2I_CONFIG","server_port").strip("")
		return self.SUCCESS

	def init_port (self):
		dev = RF_Device_Init()
		self.device = dev.init_device(self._port, self._baudrate, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE, None, serial.XOFF, self._rtscts, self._dsrdtr)
		return self.SUCCESS

