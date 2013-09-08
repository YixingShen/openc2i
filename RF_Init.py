#!/usr/bin/env python

__author__ = "Weqaar Janjua"
__copyright__ = "Copyright (C) 2012 SensorFlock"
__revision__ = "$Id$"
__version__ = "0.2"


from RF_Sys_Init import *
from RF_Node import *
from RF_Display_Init import *
from RF_Mesg_Handler import *
from RF_Threading import *


def main():

	''' RF <-> UART communication thread'''
	t0 = Thread_IO()
	t0.start()
	
	''' UART messages decoder thread'''
	t1 = Thread_MsgHandler()
	t1.start()

	''' C2I Command & Control Messaging thread'''
	t2 = Thread_C2I()
	t2.start()

	''' Display thread'''
	t3 = Thread_DisplayHandler()
	t3.start()

	''' Speech Engine thread'''
	t4 = Thread_C2I_Speech()
	t4.start()

if __name__ == '__main__':
	main()
