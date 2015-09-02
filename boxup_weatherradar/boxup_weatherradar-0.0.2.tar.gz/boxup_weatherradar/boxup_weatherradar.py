#!/bin/python

import ConfigParser
import requests
import os
import math
import logging

from boxup_types import Colorcodes
from boxup_types import MatrixData

# Load from config file
logger = logging.getLogger("boxup_weatherradar")
logger.info("Reading config-file...")

myconfig = ConfigParser.ConfigParser()
myconfig.read('/etc/boxup/plugins/boxup_weatherradar.cfg')

CENTER_LON = myconfig.getfloat('Location','lon')
CENTER_LAT = myconfig.getfloat('Location','lat')

url = myconfig.get('Settings','url')

DISTANCE1 = myconfig.getint('Settings','distance1')
DISTANCE2 = myconfig.getint('Settings','distance2')
DISTANCE3 = myconfig.getint('Settings','distance3')
DISTANCE4 = myconfig.getint('Settings','distance4')


class WeatherMatrixData (MatrixData):
	def setWidth(self):
		logger.warning("WeatherMatrixData is currently only supporting 8x8")
		pass
	def setHeight(self):
		logger.warning("WeatherMatrixData is currently only supporting 8x8")
		pass
	def getPx(self,x,y):
		if y in [0,7]:
			dy = DISTANCE4
		elif y in [1,6]:
			dy = DISTANCE3
		elif y in [2,5]:
			dy = DISTANCE2
		elif y in [3,4]:
			dy = DISTANCE1

		if y in [4,5,6,7]:
			dy *= -1

		if x in [0,7]:
			dx = DISTANCE4
		elif x in [1,6]:
			dx = DISTANCE3
		elif x in [2,5]:
			dx = DISTANCE2
		elif x in [3,4]:
			dx = DISTANCE1

		if x in [0,1,2,3]:
			dx *= -1

		point = self.__addKm(dx,dy)
		return self.__loadPoint(point)


	def __addKm(self,mdx,mdy):
		r_earth = 6378.0
		new_latitude  = CENTER_LAT  + (mdy / r_earth) * (180 / math.pi)
		new_longitude = CENTER_LON + (mdx / r_earth) * (180 / math.pi) / math.cos(CENTER_LAT * math.pi/180)
		return {'lat' : new_latitude, 'lon' : new_longitude}
		
	def __loadPoint(self,point):
		lat = point['lat']
		lon = point['lon']
		try:
			logger.info("Sending request: "+url.format(str(lat), str(lon)))
			r = requests.get(url.format(str(lat), str(lon)))
			obj = r.json()
			weather = obj['weather']
			category = weather[0]['main']
			return myconfig.getint('Categories',category)
		except Exception as e:
			logger.warning("Get no or error response to url: "+url.format(str(lat),str(lon)))
			logger.warning(e)
			return Colorcodes.OFF
		

