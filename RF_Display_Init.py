#!/usr/bin/env python

import sys
sys.path[:0] = ['./']
import os
import time
from Tkinter import *
import tkMessageBox
from guiloop import *
import Pmw
from gtkvlc import *
import threading
from RF_Node_DB import *
from RF_Node import *
from RF_Display_Queue import *
from RF_SensorList_Queue import *
import urllib
import simplekml
import signal
from socket import *

class RF_Display_Init (object):
	display_var = ":0.0"
	root = None
	top = None
	main_frame = None
	top_frame= None
	right_frame = None
	left_frame = None
	title = "SensorFlock UGS C2I Console"
	mesg_queue = None
	_pmw = None
	rwq_object = None
	sensorlist_object = None
        kmlfile = 'uag.kml'

	def __init__(self):
		self.init_display()
		self.progress_bar()
		global _node_db
		_node_db = RF_Node_DB()
		global sensor_node_db
		sensor_node_db = _node_db.sensor_node_db
		global root
		root = Tk()
		w, h = root.winfo_screenwidth(), root.winfo_screenheight()
		root.lower()
		root.wm_attributes("-fullscreen", 1)
		root.geometry("%dx%d+0+0" % (w, h))
		self.display_top_frame()
		self.display_right_frame()
		self.display_left_frame()
		self.display_button_bar()
		self.display_console_messages()
		global kml
		kml = simplekml.Kml()
		root.mainloop()

	def init_display (self):
		os.putenv('DISPLAY', self.display_var)

	def display_frame(self):
		root.protocol("WM_DELETE_WINDOW", self.callback)
		root.title(self.title)
		global main_frame
		main_frame = Frame(root, bg='white', highlightcolor='green', takefocus=1)
		main_frame.pack(fill='x')

	def display_top_frame(self):
	        global top_frame
		top_frame = Frame(root, height=200, width=1680, bg='black', highlightcolor='yellow', takefocus=1, relief='raised')
		top_frame.grid_propagate(0)
	        top_frame.grid(row=0, column=0, sticky=E+W+N+W, rowspan=2, columnspan=3)
	        self.display_bg()
													

	def display_right_frame(self):
		global right_frame
		right_frame = Frame(root, height=850, width=1300, bg='black', highlightcolor='yellow', takefocus=1, relief='raised')
		right_frame.grid_propagate(0)
		right_frame.grid(row=2, column=1, sticky=E+W+N+W, rowspan=20, columnspan=2)
		#self.display_bg()
	
	def display_left_frame(self):
		global left_frame
		left_frame = Frame(root, height=850, width=380, bg='black', highlightcolor='blue', takefocus=1, relief='raised')
		left_frame.grid_propagate(0)
		left_frame.grid(row=2, column=0, sticky=NW, rowspan=20)
	
	def display_button_bar(self):
		about = Button(self.left_frame, text="About", relief='groove', width=8, command=self.about_mesg, activeforeground='green')
		about.grid(row=5)
		a = Button(self.left_frame, text="Sensor List", relief='groove', width=8, command=self.sensor_list, activeforeground='green')
		a.grid(row=7)
		b = Button(self.left_frame, text="GIS Refresh", relief='groove', width=8, command=self.GE, activeforeground='green')
		b.grid(row=9)
		e = Button(self.left_frame, text="Thermal Video", relief='groove', width=8, command=self.thermal_video, activeforeground='green')
		e.grid(row=13)
		c = Button(self.left_frame, text="MAP", relief='groove', width=8, command=self.get_sensor_location_all, activeforeground='green')
		c.grid(row=11)
		d_img = PhotoImage(file="images/logout.gif")
		d = Button(self.left_frame, image=d_img, relief=FLAT, command=self.shutprocess, bg='black', activebackground='black', activeforeground='black', highlightcolor='black')
		d.grid(row=15)
		d.image = d_img
			

	def display_bg(self):
		img = PhotoImage(file="images/sflogo.gif")
		w = Label(self.top_frame, image=img, bg='black', activebackground='black', bd=0, fg='black')
		w.grid(row=0, column=0, columnspan=3, rowspan=1, sticky=W+E+N+S, padx=1, pady=1)
		w.image = img
				
		'''
		imgButton = Button(self.top_frame, image=img, bg='black', activebackground='black', bd=0, fg='black', state=DISABLED)
		imgButton.grid(row=0, column=0, columnspan=3, rowspan=1, sticky=W+E+N+S, padx=1, pady=1)
		imgButton.image = img
		'''

	def display_console_messages(self):
		global v
		v = StringVar()
		T = Message(bg='black', fg='green', width=360, textvariable=v)
		v.set("UGS Console: [Authorized Access]\n")
		T.grid(row=2, column=1, rowspan=10, sticky=N+S+E+W)
		''' Display thread'''
		Thread_ConsoleMessagesHandler(v).start()

	def display_full_console (self):
		global T
		T = Text(self.right_frame)
		T.focus_set()
		s = Scrollbar(self.right_frame)
		s.config(command=T.yview, highlightbackground='black', highlightcolor='black', troughcolor='black')
		T.config(yscrollcommand=s.set, bg='black', fg='green', width=51, height=17)
		s.grid(row=2, column=2, sticky=N+S, rowspan=18)
		T.grid(row=2, column=1, rowspan=18, sticky=N+S+E+W)
		Thread_ConsoleMessagesHandler(T).start()


	def display_node_db(self):
		for i, item in enumerate(sensor_node_db):
			print item['name']


	def ok(self):
		print "value is", self.e.get()
		root.destroy()

	def destroy_me(self, parent):
		parent.destroy()

	def callback(self):
		if tkMessageBox.askokcancel("Quit", "Do you really wish to quit?"):
			root.destroy()

	def shutprocess(self):
                tkMessageBox.showinfo("Terminate Process", "\n\nProcess shutdown in progress...\n")
		os.kill(os.getpid(), signal.SIGHUP)

        def about_mesg(self):
                tkMessageBox.showinfo("About C2I", "\n\nDesigned & Developed by SensorFlock\n")

	def sensor_info(self, item):
		root2 = Tk()
		text = str('MAC:' + '\t\t' + item['mac'] + '\n' + 'Name:' + '\t\t' + item[ 'name'] + '\n' + 'Mesg. Timestamp:' + '\t' + item['mesg_timestamp'] + '\n' + 'Sub-sensors:' + '\t' + str(item['sub_sensors']) + '\n' + 'Active:' + '\t\t' + item['active'] + '\n' + 'Alert Timestamp:' + '\t' + item['alert']['alert_timestamp'] + '\n' + 'Alert Type:' + '\t' + item['alert']['alert_type'] + '\n' + 'Alert Sub-sensor ID:' + '\t' + item['alert']['alert_subsensor_id'] + '\n' + 'Alert Count:' + '\t' + str(item['alert']['alert_count']) + '\n' + 'GPS Coordinates:' + '\t' + str(item['node_location'][0]))
		w = Label(root2, text=text, justify=LEFT, fg='red', bg='white')
		w.text="Sensors Info."
		w.pack()
		root2.mainloop()

	def sensor_list(self):
		parent = Tk()
		root.lower()
		parent.lift()
		_pmw = Pmw
		_pmw.initialise(parent)
		self.box = _pmw.ScrolledListBox(parent,
                items=(''),
                labelpos=N+W,
                label_text='Sensors',
                listbox_height = 6,
                selectioncommand=self.selectionCommand,
                dblclickcommand=self.defCmd,
                usehullsize = 1,
                hull_width = 50,
                hull_height = 100
        	)
		buttonBox = _pmw.ButtonBox(parent)
		buttonBox.pack(side = 'bottom')
		buttonBox.add('Refresh', text = 'Refresh', command = self.refresh_sensor_list)
		buttonBox.add('Info', text = 'Info', command = self.get_sensor_info)
		buttonBox.add('Locate', text = 'Locate', command = self.get_sensor_location)
		buttonBox.add('Exit', text = 'Exit', command = lambda:parent.destroy())
		self.box.pack(fill = 'both', expand = 1, padx = 2, pady = 2)
		self.refresh_sensor_list()

	def refresh_sensor_list(self):
		for i, item in enumerate(sensor_node_db):
			if (self.box.get(i) != item['name']):
				self.box.insert(i, item['name'])
	
	def get_sensor_info(self):
		sels = self.box.getcurselection()
		if len(sels) != 0:
			for i, item in enumerate(sensor_node_db):
				if item['name'] == sels[0]:
					self.sensor_info(item)

	'''
	coords = 'lat, long'
	'''
	def get_sensor_location(self):
		sels = self.box.getcurselection()
		if len(sels) != 0:
			if len(sensor_node_db) == 0:
				tkMessageBox.showwarning("Database Error", "Sensor Database is Empty!")
			for i, item in enumerate(sensor_node_db):
				if item['name'] == sels[0]:
					if (item['node_location'][0][0] == '0') or (item['node_location'][0][1] == '0'):
						tkMessageBox.showwarning("GPS Data Invalid", "Sensor Name: " + item['name'] + "\n\nGPS coordinates are Lat: " + item['node_location'][0][0]  + " Long: " + item['node_location'][0][1] + "\n")
					else:
						self.display_sensor_location(item)


	def GE(self):
		if len(sensor_node_db) == 0:
			tkMessageBox.showwarning("Database Error", "Sensor Database is Empty!")
		for i, item in enumerate(sensor_node_db):
			if (item['node_location'][0][0] == '0') or (item['node_location'][0][1] == '0'):
				pass
			else:
				_description = "Sensor Name: " + item['name'] + "\n" + "Lat: " + item['node_location'][0][0] + "\n" + "Long: " + item['node_location'][0][1] + "\n" + "Active: " + item['active'] + "\n" + "Alert count: " + str(item['alert']['alert_count'])
				db_node = kml.newpoint(name=item['name'], coords=[(float(item['node_location'][0][1]), float(item['node_location'][0][0]))], description=_description)
				db_node.style.iconstyle.scale = 2
				db_node.style.iconstyle.icon.href = 'http://devices.sensorflock.com/icons/uag-icon.gif'
                      		kml.save(self.kmlfile)
	def thermal_video (self):
		url = "http://192.168.15.4:8080/uag"
		p=VideoPlayer()
        	p.main(url)

	def get_sensor_location_all(self):
		all_info_list = []
		if len(sensor_node_db) == 0:
			tkMessageBox.showwarning("Database Error", "Sensor Database is Empty!")
		for i, item in enumerate(sensor_node_db):
			if (item['node_location'][0][0] == '0') or (item['node_location'][0][1] == '0'):
				pass
			else:
				all_info_list.append(item['node_location'][0]) #list of coords ['0', '1', '2']
		if len(all_info_list) != 0:
			self.display_sensor_location_all(all_info_list)
		else:
			tkMessageBox.showwarning("GPS Data Invalid", "\n\nGPS coordinates for all sensors are Lat: 0, Long: 0\n")


	def display_sensor_location(self, item):
		#coordinates: lat, long
		coords = item['node_location'][0][0] + ',' + item['node_location'][0][1]
		map_file = self.get_googlemap(coords)
		if map_file is False:
			tkMessageBox.showerror("Network Connection Error", "\n\nUnable to connect to \nGoogle Maps Web Service\n")
			return False
		root3 = Tk()
		map_image = PhotoImage(file=str(map_file), master=root3)
		label = Label(root3, image=str(map_image))
		label.image = str(map_image) # keep a reference!
		label.pack()
		root3.mainloop()

	def display_sensor_location_all(self, all_info_list):
		#coordinates: lat, long
		if len(all_info_list) == 0:
			print "all_info_list is Empty\n"
		map_file = self.get_googlemap_all(all_info_list)
		if map_file is False:
			tkMessageBox.showerror("Network Connection Error", "\n\nUnable to connect to \nGoogle Maps Web Service\n")
			return False
		root3 = Tk()
		map_image = PhotoImage(file=str(map_file), master=root3)
		label = Label(root3, image=str(map_image))
		label.image = str(map_image) # keep a reference!
		label.pack()
		root3.mainloop()


	def get_googlemap(self, coords):
		map_file = './maps/map-' + coords + '.gif'
		host = 'maps.google.com'
		port = 80
		if not self.test_network(host, port):
			return False
		base_url = 'http://' + host + '/maps/api/staticmap?'
		zoom = '14'
		size = '800x600'
		sensor = 'sensor=true'
		maptype = 'roadmap'
		img_format = 'gif'
		markers = 'icon:http://devices.sensorflock.com/icons/uag-icon.gif|color:red|label:S|'
		amp = '&'
		_url = base_url + 'zoom=' + zoom + amp + 'size=' + size + amp + sensor + amp + 'maptype=' + maptype + amp + 'format=' + img_format + amp + 'markers=' + markers + coords
		if os.path.exists(map_file):
			return map_file
		(filename, headers) = urllib.urlretrieve (_url, map_file)
		return filename

	def get_googlemap_all(self, coords_list):
		url_string = ''
		map_file = './maps/map-' + str(time.clock()) + '.gif'
		host = 'maps.google.com'
		port = 80
		if not self.test_network(host, port):
			return False
		base_url = 'http://' + host + '/maps/api/staticmap?'
		zoom = '12'
		size = '1024x800'
		sensor = 'sensor=true'
		maptype = 'hybrid'
		img_format = 'gif' 
		markers = 'icon:http://devices.sensorflock.com/icons/uag-icon.gif|color:red|'
		amp = '&'
		for item in coords_list:
			url_string = url_string + 'markers=' + markers + item[0] + ',' + item[1] + amp
		_url = base_url + 'zoom=' + zoom + amp + 'size=' + size + amp + sensor + amp + 'maptype=' + maptype + amp + 'format=' + img_format + amp + url_string
		(filename, headers) = urllib.urlretrieve (_url, map_file)
		urllib.urlcleanup()
		return filename

	def _reporthook(self, blocks_read, block_size, total_size):
		if not blocks_read:
			v.set('Connection opened')
			return
		if total_size < 0:
		# Unknown size
			v.set('Read blocks: ' + str(blocks_read))
		else:
			v.set('Percent Completed: ' + str(int(blocks_read*block_size*100/total_size)) + '%')
		return

	def test_network(self, ip_address, port, timeout=3):
		s = socket(AF_INET, SOCK_STREAM)
		s.settimeout(timeout)
		result = s.connect_ex((ip_address, port))
		s.close()
		if(result == 0):
			return True
		else:
			return False

	def showYView(self):
		w = Tkinter.Label(root, text="Hello, world!")
		w.pack()
		print self.box.yview()
	
	def selectionCommand(self):
		print "def selectionCommand(self)\n"
		sels = self.box.getcurselection()
		if len(sels) == 0:
			print 'No selection'
		else:
			print 'Selection:', sels[0]

	def defCmd(self):
		sels = self.box.getcurselection()
		if len(sels) == 0:
			print 'No selection for double click'
		else:
			print 'Double click:', sels[0]


	def progress_bar(self):
		global root
		root = Tkinter.Tk(className='UGS - C2I Engine Boot Progress')
		root.wm_overrideredirect(True)
		w = 480
		h = 20
		ws = root.winfo_screenwidth() - 50
		hs = root.winfo_screenheight()
		x = (ws/2) - (w/2)
		y = (hs/2) - (h/2)
		root.geometry('%dx%d+%d+%d' % (w, h, x, y))
		m = Meter(root, relief='raised', bd=1)
		m.pack(fill='x')
		m.set(0.0, 'Booting UGS Engine...')
		m.after(1000, lambda: self._bardemo(m, 0.0))
		root.mainloop()

	def _bardemo(self, meter, value):
		meter.set(value)
		if value < 1.0:
				value = value + 0.025
				meter.after(50, lambda: self._bardemo(meter, value))
		else:
			meter.set(value, 'Done.')
			time.sleep(0.5)
			root.destroy()


class Thread_ConsoleMessagesHandler(threading.Thread):

	_var = None

	def __init__(self, v):
		threading.Thread.__init__(self)
		global rwq_object
		rwq_object = RF_Display_Queue()
		self._var = v

	def run(self):
		while True:
			if rwq_object.is_empty() is False:
				_txtvar = rwq_object.get()
				self._var.set(_txtvar)

