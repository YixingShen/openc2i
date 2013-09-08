#!/usr/bin/env python

import threading
import time
import socket
import RF_Server
import pyttsx
from RF_Sys_Init import *
from RF_Mesg_Handler import *
from RF_Display_Init import *
from RF_Speech_Queue import *
from RF_IO_Queue import *
import multiprocessing

'''Global Vars'''
queue = None
c2i_queue = None
display_queue = None
_rf_init = None
_mesg_handler = None
rw_queue = None

'''Class Definitions'''
class Thread_IO(threading.Thread):

	def __init__(self):
		threading.Thread.__init__(self)
		global _rf_init
		_rf_init = RF_Sys_Init()
		global queue, c2i_queue, display_queue, rw_queue
		queue = multiprocessing.Queue()
		c2i_queue = multiprocessing.Queue()
		display_queue = multiprocessing.Queue()
		rw_queue = multiprocessing.Queue()
		global io_queue
		io_queue = RF_IO_Queue()

	def run(self):
		_rf_init.config_parser()
		while True:
			if not io_queue.is_empty():
				mesg = io_queue.get()
				'''Insert message into Queue and remove from buffer. Block queue when writing'''
				queue.put(mesg.strip(), block=True, timeout=None)


class Thread_MsgHandler(threading.Thread):

	def __init__(self):
		threading.Thread.__init__(self)
		global _mesg_handler
		_mesg_handler = RF_Mesg_Handler()

	def run(self):
		while True:
			if not queue.empty():
				queue_mesg = queue.get() 
				'''print "Message Received from SerialPort: " + queue_mesg + "\n"'''
				'''we insert the messages into c2i_queue here but not in Thread_IO since this might Block Thread_IO thread.'''
				c2i_queue.put(queue_mesg, block=True, timeout=None)
				display_queue.put(queue_mesg, block=True, timeout=None)
				_mesg_handler.mesg_decode(queue_mesg)
			else:
				pass


class Thread_C2I(threading.Thread):

	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		while _rf_init._c2i_server_ip is None: 
			pass
		while _rf_init._c2i_server_port is None: 
			pass
		RF_Server.start_server(_rf_init._c2i_server_ip, _rf_init._c2i_server_port)


class Thread_C2I_Speech(threading.Thread):
        speech_object = None
	_txtvar = None

	def __init__(self):
		threading.Thread.__init__(self)
		global speech_object, _txtvar
                speech_object = RF_Speech_Queue()


	def run(self):
		while True:
			if speech_object.is_empty() is False:
				self.say(speech_object.get())
                		#_txtvar = speech_object.get()
				#print "_txtvar: " + _txtvar
				#_txtvar = ''

	def say(self, __txtvar):
		tts = pyttsx.init(driverName='espeak')
                rate = tts.getProperty('rate')
                tts.getProperty('voices')
                tts.setProperty('voice', 'english_us')
                tts.setProperty('rate', rate-35)
                tts.say(__txtvar)
                tts.runAndWait()
		tts.stop()
		

class Thread_DisplayHandler(threading.Thread):

	_display_handler = None

	def __init__(self):
		threading.Thread.__init__(self)
		global _display_handler

	def run(self):
		_display_handler = RF_Display_Init()


