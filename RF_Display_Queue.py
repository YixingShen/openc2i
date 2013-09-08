'''
Created on Feb 11, 2012

@author: weqaar
'''
import multiprocessing

class RF_Display_Queue (object):
   	rw_queue = None

	def __init__ (self):
        	global rw_queue
        	rw_queue = multiprocessing.Queue() 

	def put (self, data):
		'''rw_queue.put(data, block=True, timeout=None)'''
		rw_queue.put(data)

	def get (self):
		return rw_queue.get()

	def is_empty (self):
		if rw_queue.empty():
			return True
		else:
			return False

