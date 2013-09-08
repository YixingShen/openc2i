#!/usr/bin/env python

import threading

'''Class Definitions'''
class Thread_Event(object):

	thread_event = None

	def __init__(self):
		global thread_event
        	thread_event = threading.Event()

	def setflag(self):
		thread_event.set()

	def clear(self):
		thread_event.clear()

	def wait(self):
		#while not thread_event.isSet():
            	thread_event.wait()

