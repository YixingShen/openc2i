'''
Created on Feb 19, 2012

@author: weqaar
'''
import simplekml

class RF_Kml (object):
	kml_file = 'uag.kml' 
 
	def __init__ (self):
		global kml
		kml = simplekml.Kml()
       
	def create_point(self, _name, _coords, _description):
		pnt = kml.newpoint(name=_name, coords=_coords, description=_description)
		pnt.iconstyle.icon.href = 'http://devices.sensorflock.com/icons/uag-icon.gif'

	def save_file(self):
		kml.save(self.kml_file)
