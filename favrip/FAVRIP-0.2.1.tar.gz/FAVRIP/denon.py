#!/usr/bin/env python
# -*- coding:utf-8 -*

'''
Class denonAVR

	Pour communication avec AVR Denon
	
	Models :
	Models :
		- AVR-3311CI
		- AVR-3311
		- AVR-991
		- AVR-X2100W (tested)
		- ...

'''
import socket
import functools
import time
import re
from favrip import *

class denonAVR(favrip):
	'''Un ampli Video DENON
	'''
	COMMANDS = {
		'Power': {
		'on': 'PWON',
		'off': 'PWSTANDBY',
		'get' : 'PW?'
		},
		'MasterVolume': {
		'up': 'MVUP',
		'down': 'MVDOWN',
		'set': 'MV%02i',
		'get': 'MV?'
		},
		'Mute': {
		'on': 'MUON',
		'off': 'MUOFF'
		},
		'Input': {
		'phono': 'SIPHONO',
		'cd': 'SICD',
		'tuner': 'SITUNER',
		'dvd': 'SIDVD',
		'bluray': 'SIBD',
		'tv': 'SITV',
		'cable': 'SISAT/CBL',
		'dvr': 'SIDVR',
		'game': 'SIGAME',
		'game2': 'SIGAME2',
		'v.aux': 'SIV.AUX',
		'aux1': 'SIAUX1',
		'aux2': 'SIAUX2',
		'mplay': 'SIMPLAY',
		'usb': 'SIUSB/IPOD',
		'ipod': 'SIIPOD DIRECT',
		'dock': 'SIDOCK',
		'net_usb': 'SINET/USB',
		'lastfm': 'SILASTFM',
		'net': 'SINET',
		'bt': 'SIBT',
		'flickr': 'SIFLICKR',
		'favorites': 'SIFAVORITES',
		'iradio': 'SIIRADIO',
		'server': 'SISERVER',
		'get': 'SI?'
		},
		'InputAndPlay': {
		'ipod': 'SIIPOD',
		'usb': 'SIUSB',
		'ipod_direct': 'SIIPD',
		'iradio': 'SIIRP',
		'favorites': 'SIFVR'
		},
		'MainZone': {
		'on': 'ZMON',
		'off': 'ZMOFF',
		'get': 'ZM?'
		},
		'SleepTimer': {
		'off': 'SLPOFF',
		'on': 'SL%02i'
		}
		}
	
	def on(self):
		'''Set on the AVR, only MainZone
		'''
		self.execute('MainZone','on')
	
	def off(self):
		'''Set off the AVR, only MainZone
		'''
		self.execute('MainZone','off')
	
	@favrip.trys
	def get_power(self):
		''' Return 'on' ou 'off' '''
		reponse =  self.execute('MainZone', 'get')
		if re.match(r'ZMON', reponse):
			return 'on'
		elif re.match(r'ZMOFF', reponse):
			return 'off'
		else:
			raise socket.error
	
	@favrip.trys
	def get_volume(self):
		'''Get the  Volume'''
		reponse = self.execute('MasterVolume', 'get')
		return int(reponse[2:4])
	
	@favrip.trys
	def get_input(self):
		''' Get the input source'''
		reponse = self.execute('Input', 'get')
		reponse = re.findall(r'SI[A-Z0-9]+', reponse)[0][2:]
		for cle, cmd in self.COMMANDS['Input'].items():
			if 'SI'+reponse==cmd:
				return cle

#########################################################
#                                                       #
#		EXEMPLE                                         #
#                                                       #
#########################################################

if __name__ == '__main__':
	ampli = denonAVR('192.168.10.175')
	ampli.on()
	ampli.set_aux2()