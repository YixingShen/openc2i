#!/usr/bin/env python

class RF_Node (object):
	FOUND = DONE = 1
	NOT_FOUND = ERROR = 0

	def __init__ (self):
		self.sensor_node = {}
		self.sensor_node_obj_def = {	'mac' : '',
										'mesg_timestamp' : '',
										'name' : '',
										'sub_sensors' : 0,
										'active' : '',
										'alert' : {	'alert_timestamp' : '',
													'alert_type' : '',
													'alert_subsensor_id' : '',
													'alert_count' : 0 
													},
										'node_location' : [['0', '0', '0']] #[lat, long, altitude] LIST
										}

	def add_sensor (self, sensor_node_obj, sensor_node_db):
		if self.find_sensor(sensor_node_obj, sensor_node_db)[0] == self.FOUND:
			return self.ERROR
		else:
			sensor_node_obj['alert']['alert_count'] = 0 #Initialize 'alert_count' to 0
			sensor_node_db.append(sensor_node_obj)
			return self.DONE

	def find_sensor (self, sensor_node_obj, sensor_node_db):
		if len(sensor_node_db) is 0:
			return (self.NOT_FOUND, -1)
		
		for i, item in enumerate(sensor_node_db):
			if item['mac'] == sensor_node_obj['mac']:
				return (self.FOUND, i)
		
		return (self.NOT_FOUND, -1)
		

	def update_sensor (self, sensor_node_obj, sensor_node_db):
		find_status = self.find_sensor(sensor_node_obj, sensor_node_db)
		if find_status[0] == self.FOUND:
			#check mesg_timestamp
			if (sensor_node_db[find_status[1]]['mesg_timestamp'] != sensor_node_obj['mesg_timestamp']) and (sensor_node_obj['mesg_timestamp'] != ''):
				sensor_node_db[find_status[1]]['mesg_timestamp'] = sensor_node_obj['mesg_timestamp']
			#check name
			'''
			if (sensor_node_db[find_status[1]]['name'] != sensor_node_obj['name']) and (sensor_node_obj['name'] != ''):
				sensor_node_db[find_status[1]]['name'] = sensor_node_obj['name']
			'''
			#check sub_sensors
			'''
			if (sensor_node_db[find_status[1]]['sub_sensors'] != sensor_node_obj['sub_sensors']):
				sensor_node_db[find_status[1]]['sub_sensors'] = sensor_node_obj['sub_sensors']
			'''
			#check if active
			if (sensor_node_db[find_status[1]]['active'] != sensor_node_obj['active']) and (sensor_node_obj['active'] != ''):
				sensor_node_db[find_status[1]]['active'] = sensor_node_obj['active']
			#check alert_timestamp
			#if (sensor_node_db[find_status[1]]['alert']['alert_timestamp'] != sensor_node_obj['alert']['alert_timestamp']) and (sensor_node_obj['alert']['alert_timestamp'] != ''):
			if sensor_node_obj['alert']['alert_timestamp'] != '':
				sensor_node_db[find_status[1]]['alert']['alert_timestamp'] = sensor_node_obj['alert']['alert_timestamp']
				#Increment Alert Count
				sensor_node_db[find_status[1]]['alert']['alert_count'] += 1
			#check alert_type
			if (sensor_node_db[find_status[1]]['alert']['alert_type'] != sensor_node_obj['alert']['alert_type']) and (sensor_node_obj['alert']['alert_type'] != ''):
				sensor_node_db[find_status[1]]['alert']['alert_type'] = sensor_node_obj['alert']['alert_type']
			#check alert_subsensor_id
			if (sensor_node_db[find_status[1]]['alert']['alert_subsensor_id'] != sensor_node_obj['alert']['alert_subsensor_id']) and (sensor_node_obj['alert']['alert_subsensor_id'] != ''):
				sensor_node_db[find_status[1]]['alert']['alert_subsensor_id'] = sensor_node_obj['alert']['alert_subsensor_id']
			#check node_location[s]
			#First time update object
			if (sensor_node_obj['node_location'][0] != ['0', '0', '0']) and (sensor_node_db[find_status[1]]['node_location'][0] == ['0', '0', '0']):
				sensor_node_db[find_status[1]]['node_location'].pop(0)
				#Manipulate GPS coords here
				sensor_node_db[find_status[1]]['node_location'].insert(0, (sensor_node_obj['node_location'][0]))
			#Previously updated object, but old location is not the same is new location
			elif sensor_node_db[find_status[1]]['node_location'][0] != sensor_node_obj['node_location'][0]:
				if sensor_node_obj['node_location'][0] != ['0', '0', '0']:
					#Manipulate GPS coords here
					sensor_node_db[find_status[1]]['node_location'].insert(0, (sensor_node_obj['node_location'][0]))
				elif sensor_node_obj['node_location'][0] == ['0', '0', '0']:
					pass
			return self.DONE
		else: 
			'''self.add_sensor(sensor_node_obj)'''
			return self.ERROR
	
	def remove_sensor (self, sensor_node_obj, sensor_node_db):
		find_status = self.find_sensor(sensor_node_obj, sensor_node_db)
		if find_status[0] == self.FOUND:
			sensor_node_db.pop(find_status[1])
			return self.DONE
		else:
			return self.ERROR

	'''Returns:
		LIST [] that includes data on all Sensor Nodes
	'''
	def list_sensors (self, sensor_node_db):
		ret_sensor_db = []
		for i in range(len(sensor_node_db)):
			'''check for empty sensor_node_db'''
			ret_sensor_db.append(sensor_node_db[i])
		return ret_sensor_db

