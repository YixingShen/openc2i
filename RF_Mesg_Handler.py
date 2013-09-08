#!/usr/bin/env python

import random
import time
import binascii
import os
import string
from RF_Node_DB import *
from RF_Node import *
from RF_Display_Queue import *
from RF_Speech_Queue import *
from RF_SensorList_Queue import *

class RF_Mesg_Handler (object):
	_type_field_separator = ":"
	_content_field_separator = ","
	MAC = None
	MESG_TYPE = None
	ALERT_TYPE = None
	rwq_object = None
	speech_object = None
	sensorlist_object = None

	def __init__ (self):
		global _node_db
		_node_db = RF_Node_DB()
		global sensor_node_db
		sensor_node_db = _node_db.sensor_node_db
		self.rwq_object = RF_Display_Queue()
		self.speech_object = RF_Speech_Queue()
		self.sensorlist_object = RF_SensorList_Queue()
		self.MAC = 'mac'
		self.MESG_TYPE = ['SENSOR_JOINED', 'SENSOR_LOCATION', 'ALERT', 'SENSOR_DISCONNECTED']
		self.ALERT_TYPE = ['Motion', 'Vibration']

	'''
	TODOs: change sensor_obj.sensor_node_obj_def['name'] to read real name instead of a random generated
	'''
	def mesg_decode (self, orig_mesg):
		self.sensor_obj = RF_Node()

		_mesg = self.validate_mesg(orig_mesg)
		if _mesg is False:
			return False
		else:
			mac = _mesg[0]
			mesg_type = _mesg[1]
			if _mesg[2] != None:
				payload = _mesg[2]

		print "mac: " + mac
		print "mesg_type: " + mesg_type
		if _mesg[2] != None:
			print "payload: " + payload
 
		#Construct Sensor Node Object
		self.sensor_obj.sensor_node_obj_def['mac'] = mac
		self.sensor_obj.sensor_node_obj_def['mesg_timestamp'] = time.ctime()
		if self.sensor_obj.find_sensor(self.sensor_obj.sensor_node_obj_def, sensor_node_db)[0] == self.sensor_obj.NOT_FOUND:
			self.sensor_obj.sensor_node_obj_def['name'] = 'uag' + binascii.b2a_hex(os.urandom(1))
			self.sensor_obj.sensor_node_obj_def['sub_sensors'] = random.randint(1,4)
				
		#SENSOR_JOINED
		if mesg_type == self.MESG_TYPE[0]: 			
			if self.sensor_obj.find_sensor(self.sensor_obj.sensor_node_obj_def, sensor_node_db)[0] == self.sensor_obj.NOT_FOUND:
				self.sensor_obj.sensor_node_obj_def['active'] = 'Y'
				self.sensor_obj.sensor_node_obj_def['alert']['alert_timestamp'] = time.ctime()
				self.sensor_obj.sensor_node_obj_def['alert']['alert_type'] = 'NA'
				self.sensor_obj.sensor_node_obj_def['alert']['alert_subsensor_id'] = 'NA'
				self.sensor_obj.sensor_node_obj_def['node_location'][0] = ['0', '0', '0']
				self.sensor_obj.add_sensor(self.sensor_obj.sensor_node_obj_def, sensor_node_db)
				self.sensorlist_object.put(self.sensor_obj.sensor_node_obj_def)
				return "#SENSOR_JOINED sensor_obj NOT FOUND: " + self.MESG_TYPE[0]
			else:
				self.sensor_obj.sensor_node_obj_def['active'] = 'Y'
				self.sensor_obj.update_sensor(self.sensor_obj.sensor_node_obj_def, sensor_node_db)
				return "#SENSOR_JOINED sensor_obj FOUND: " + self.MESG_TYPE[0]

		#ALERT
		if mesg_type == self.MESG_TYPE[2]:
			self.sensor_obj.sensor_node_obj_def['active'] = 'Y'
			self.sensor_obj.sensor_node_obj_def['alert']['alert_timestamp'] = time.ctime()
			self.sensor_obj.sensor_node_obj_def['alert']['alert_type'] = payload.split(self._content_field_separator, 1)[0]
			self.sensor_obj.sensor_node_obj_def['alert']['alert_subsensor_id'] = payload.split(self._content_field_separator, 1)[1]
			'''self.rwq_object.put(mesg_type + self._type_field_separator + ' ' + sensor_node_db[self.sensor_obj.find_sensor(self.sensor_obj.sensor_node_obj_def, sensor_node_db)[1]]['name'] + self._type_field_separator + ' ' + self.sensor_obj.sensor_node_obj_def['alert']['alert_type'] + self._type_field_separator + ' ' + self.sensor_obj.sensor_node_obj_def['alert']['alert_subsensor_id'])
				'''
			if self.sensor_obj.find_sensor(self.sensor_obj.sensor_node_obj_def, sensor_node_db)[0] == self.sensor_obj.NOT_FOUND:
				return "#ALERT sensor_obj NOT FOUND: " + self.MESG_TYPE[2]
			else:
				self.rwq_object.put("[" + self.sensor_obj.sensor_node_obj_def['alert']['alert_timestamp'] + "]\n\n" + mesg_type + self._type_field_separator + ' ' + sensor_node_db[self.sensor_obj.find_sensor(self.sensor_obj.sensor_node_obj_def, sensor_node_db)[1]]['name'] + self._type_field_separator + ' ' + self.sensor_obj.sensor_node_obj_def['alert']['alert_type'] + self._type_field_separator + ' ' + self.sensor_obj.sensor_node_obj_def['alert']['alert_subsensor_id'])
				self.speech_object.put(mesg_type + self._type_field_separator + ' ' + sensor_node_db[self.sensor_obj.find_sensor(self.sensor_obj.sensor_node_obj_def, sensor_node_db)[1]]['name'] + self._type_field_separator + ' ' + self.sensor_obj.sensor_node_obj_def['alert']['alert_type'] + self._type_field_separator + ' ' + self.sensor_obj.sensor_node_obj_def['alert']['alert_subsensor_id'])
				self.sensor_obj.update_sensor(self.sensor_obj.sensor_node_obj_def, sensor_node_db)
				return "#ALERT sensor_obj FOUND: " + self.MESG_TYPE[2]

		#SENSOR_LOCATION
		if mesg_type == self.MESG_TYPE[1]:
			'''self.sensor_obj.sensor_node_obj_def['mac'] = mac'''
			if self.sensor_obj.find_sensor(self.sensor_obj.sensor_node_obj_def, sensor_node_db)[0] == self.sensor_obj.NOT_FOUND:
				return "#SENSOR_LOCATION sensor_obj NOT FOUND: " + self.MESG_TYPE[1]
			else:
				self.sensor_obj.sensor_node_obj_def['active'] = 'Y'
				#Modify GPS coordinates here:
				gps_coords = self.kill_murphy([payload.split(self._content_field_separator, 2)[0],payload.split(self._content_field_separator, 2)[1],payload.split(self._content_field_separator, 2)[2]])
				print "gps_coords: " + str(gps_coords)
				self.sensor_obj.sensor_node_obj_def['node_location'].insert(0, gps_coords)
				'''self.sensor_obj.sensor_node_obj_def['node_location'].insert(0, [payload.split(self._content_field_separator, 2)[0],payload.split(self._content_field_separator, 2)[1],payload.split(self._content_field_separator, 2)[2]])'''
				self.sensor_obj.update_sensor(self.sensor_obj.sensor_node_obj_def, sensor_node_db)
				return "#SENSOR_LOCATION sensor_obj FOUND: " + self.MESG_TYPE[1]

		#SENSOR_DISCONNECTED
		if mesg_type == self.MESG_TYPE[3]:
			'''self.sensor_obj.sensor_node_obj_def['mac'] = mac'''
			if self.sensor_obj.find_sensor(self.sensor_obj.sensor_node_obj_def, sensor_node_db)[0] == self.sensor_obj.NOT_FOUND:
				return "#SENSOR_DISCONNECTED sensor_obj NOT FOUND: " + self.MESG_TYPE[3]
			else:
				self.sensor_obj.sensor_node_obj_def['active'] = 'N'
				self.sensor_obj.update_sensor(self.sensor_obj.sensor_node_obj_def, sensor_node_db)
				print "Sensor List: " + str(self.sensor_obj.list_sensors(sensor_node_db)) + '\n'
				return "#SENSOR_DISCONNECTED sensor_obj FOUND: " + self.MESG_TYPE[3]


	'''
	Returns:
	(mac, mesg_type, payload)
	'''
	def validate_mesg(self, _mesg):
		if _mesg == '':
                	return False

		if _mesg[0] == self._type_field_separator:
			return False

		payload = None
                #MAC Address Check
                mac1 = _mesg.split(self._type_field_separator, 2)[0]
                if (mac1[0] == '0') and (mac1[1] == 'x'):
			pass
		else:
			return False

                mac2 = _mesg.split(self._type_field_separator, 2)[1]
                if (mac2[0] == '0') and (mac2[1] == 'x'):
			pass
		else:
			return False
                mac = mac1 + self._type_field_separator + mac2
                if self.valid_mac(mac) is True:
			pass
                else:
			return False
                #Message Type Check
                mesg_stripped_mac = _mesg.split(self._type_field_separator, 2)[2]
                mesg_type = mesg_stripped_mac.split(self._type_field_separator, 1)[0]
                if (mesg_type in self.MESG_TYPE):
                        pass
                else:
                        return False
                #Message Payload Check
                if (mesg_type != self.MESG_TYPE[0]) and (mesg_type != self.MESG_TYPE[3]):
                	payload = mesg_stripped_mac.split(self._type_field_separator, 1)[1]
                        if len(payload) == 0:
                                return False
                        else:
                                pass
                return (mac, mesg_type, payload)
		
	'''
	Returns:
		True: if the mac is valid
		False: if the mac is invalid
	Caveats:
		To be used for 802.15.4 MAC Addresses only (EUI-64)

	802.15.4 MAC address is an eight-byte (64 bit) value
	'''
	def valid_mac (self, _mac):
		if self._type_field_separator in _mac:
			split_mac = _mac.split(self._type_field_separator) ##List[] containing two mac parts separated by a ":"
			if (split_mac[0][0] == '0') and (split_mac[0][1] == 'x'):
				mac_part1 = split_mac[0].split("x") #List[] containing the hex part of mac separated by an "x" i.e. 0x758b14
				mac_part2 = split_mac[1].split("x") #List[] containing the hex part of mac separated by an "x" i.e. 0x758b14
			else:
				return False
		else:
			return False
		if (self.ishex(mac_part1[1])) and (self.ishex(mac_part2[1])):
			return True
		else:
			return False

			
	'''
	Source:
	http://groups.google.com/group/peachfuzz/browse_thread/thread/d35d405390628220
	'''
	def ishex(self, strValue):
		for i in strValue:
			if (i>='0' and i<='9') or (i>='a' and i<='f') or (i>='A' and i<='F'):
				continue
			else:
				return False
		return True
			

	def kill_murphy(self, gps_coords):
		'''
		gps_coords[0] = gps_coords[0][0:2] + ' ' + gps_coords[0][2:4] + '.' + filter(lambda c: c not in ".", gps_coords[0][4:])
		gps_coords[1] = gps_coords[1][0:3] + ' ' + gps_coords[1][3:5] + '.' + filter(lambda c: c not in ".", gps_coords[1][5:])
		'''
		'''
		if gps_coords[1][0] == '0':
			gps_coords[1] = gps_coords[1][0:3] + ' ' + gps_coords[1][3:5] + '.' + filter(lambda c: c not in ".", gps_coords[1][5:])
		else:
			gps_coords[1] = gps_coords[1][0:2] + ' ' + gps_coords[1][2:4] + '.' + filter(lambda c: c not in ".", gps_coords[1][4:])
		'''
		gps_coords[0] = str(self.toDecimalDegrees(gps_coords[0]))
		gps_coords[1] = str(self.toDecimalDegrees(gps_coords[1]))
		return gps_coords

	def toDecimalDegrees(self, ddmm):
    		splitat = string.find(ddmm, '.') - 2
    		return self._float(ddmm[:splitat]) + self._float(ddmm[splitat:]) / 60.0

	def _float(self, s):
		if s:
        		return float(s)
    		else:
        		return None	

