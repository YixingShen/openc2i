'''
Created on Feb 11, 2012

@author: weqaar
'''
import multiprocessing

class RF_SensorList_Queue (object):
   	sensorlist_queue = None

	def __init__ (self):
        	global sensorlist_queue
        	sensorlist_queue = multiprocessing.Queue() 

	def put (self, data):
		sensorlist_queue.put(data, block=True, timeout=None)

	def get (self):
		return sensorlist_queue.get()

	def is_empty (self):
		if sensorlist_queue.empty():
			return True
		else:
			return False

