'''
Created on Feb 24, 2012

@author: weqaar
'''
import multiprocessing

class RF_IO_Queue (object):
   	io_queue = None

	def __init__ (self):
        	global io_queue
        	io_queue = multiprocessing.Queue() 

	def put (self, data):
		'''rw_queue.put(data, block=True, timeout=None)'''
		io_queue.put(data)

	def get (self):
		return io_queue.get()

	def is_empty (self):
		if io_queue.empty():
			return True
		else:
			return False

