'''
Created on Feb 22, 2012

@author: weqaar
'''
import multiprocessing

class RF_Speech_Queue (object):
   	speech_queue = None

	def __init__ (self):
        	global speech_queue
        	speech_queue = multiprocessing.Queue() 

	def put (self, data):
		'''rw_queue.put(data, block=True, timeout=None)'''
		speech_queue.put(data)

	def get (self):
		return speech_queue.get()

	def is_empty (self):
		if speech_queue.empty():
			return True
		else:
			return False

