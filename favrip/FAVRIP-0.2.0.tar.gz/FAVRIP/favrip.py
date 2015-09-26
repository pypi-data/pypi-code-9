#!/usr/bin/env python
# -*- coding:utf-8 -*


'''
Class favrip

	Pour communication avec Audio Video Receiver IP
	
	V0.2.0 :
		cloture de la connexion au serveur àprès chaque commande

'''
import socket
import functools
import time
import threading
import logging

class favrip(object):
	''' A Audio Video Receiver with ethernet link
	'''
	def __init__(self, adr_ip, timeout = 10, port = 23):
		'''Initialisation
			- adr_ip	:	ip adress
			- timeout	:	timeout (default = 10s)
			- port		:	port (default = 23)
		'''
		self.adr_ip = adr_ip
		self.timeout = timeout
		self.port = port
		self.sock = None
		self.lock = threading.RLock()
		logging.info("Audio Video recever %s is created." % self)
		# Connection à l'ampli pour test
		self.connect()
		self.disconnect()
	
	def connect(self):
		'''Connection a l'ampli'''
		if self.sock:
			self.disconnect()
		logging.debug('connection to %s'%self)
		try:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.sock.connect((self.adr_ip, self.port))
			self.sock.settimeout(self.timeout)
		except (EOFError, socket.error, ValueError, socket.timeout), e:
			logging.error('Connection error to %s : %s' % (self, e))
			self.disconnect()
	
	def disconnect(self):
		''' Disable the connection to ampli'''
		logging.debug('(disconnection to %s'%self)
		if self.sock:
			self.sock.close()
			self.sock = None
		
	def unError(fonction):
		'''Decorateur pour 
				- eviter les erreurs
				- verrouiller l'accés à l'ampli 
		Si erreur dans une des methodes, on essaye de reconnecter le serveur 1 fois
		Si ca ne passe toujours pas, on abandonne'''
		@functools.wraps(fonction) # ca sert pour avoir un help(SBClient) utile
		def SBUnErrorFonction(self,*args, **kwargs):
			with self.lock:
				try:
					return fonction(self,*args, **kwargs)
				except Exception, e:
					logging.warning(str(e) + ' in ' + fonction.__name__)
					logging.warning("Try again ...")
					self.disconnect()
					time.sleep(0.5)
					try:
						return fonction(self,*args, **kwargs)
					except Exception, e:
						logging.error('Retry failed. ' + str(e))
						return None
		return SBUnErrorFonction
	
	@staticmethod
	def trys(fonction):
		'''Décorateur pour tester 4 fois la fonction
		'''
		@functools.wraps(fonction) # ca sert pour avoir un help(SBClient) utile
		def SBUnErrorFonction(self, trys = 4):
			with self.lock:
				if trys < 1:
					logging.error('Fatal Error (no retry) in %s' % (fonction.__name__))
					return None
				else:
					try:
						return fonction(self)
					except Exception, e:
						logging.warning('Error in %s (retry %s) : %s' % (fonction.__name__, trys, str(e)))
						SBUnErrorFonction(self, trys - 1)
		return SBUnErrorFonction
	
	@unError	
	def command(self, cmd):
		'''Execute l'action cmd
		'''
		self.connect()
		logging.debug("Command send to %s : '%s'" % (self, cmd))
		self.sock.sendall(cmd + '\r')
		time.sleep(0.25) # Pour être sur de bien lire le retour
		data = self.sock.recv(1024)
		self.disconnect()
		logging.debug("Datas received from %s : %s" % (self, data))
		return data
	
	def execute(self, command, arg, value = None):
		''' Execute a command
			- command	ex : MasterVolume
			- arg		ex : set
			- value		ex : 30
		'''
		try:
			if value == None:
				return self.command(self.COMMANDS[command][arg])
			else:
				return self.command(self.COMMANDS[command][arg] % value)
		except KeyError, e:
			logging.error("Unknow commande-arg in %s : %s-%s" % (self, command, arg))
			return 'KeyError'
	
	def on(self):
		''' Turn on the AVR'''
		self.execute('Power', 'on')
	
	def standby(self):
		''' Turn off the AVR'''
		self.execute('Power', 'off')
	
	def off(self):
		''' Turn off the AVR'''
		self.execute('Power', 'off')
	
	def set_power(self, arg='on'):
		''' Turn the power on(defaut)/off '''
		self.execute('Power', arg)
	
	def volume_up(self):
		''' Set the volume up'''
		self.execute('MasterVolume','up')
	
	def volume_down(self):
		''' Set the volume down'''
		self.execute('MasterVolume','down')
	
	def set_volume(self, volume):
		''' Set the volume'''
		self.execute('MasterVolume', 'set', volume)
	
	def set_input(self, source):
		''' Set the input source'''
		self.execute('Input', source)
	
	def set_input_and_play(self, source):
		''' Set the input source and play it'''
		self.execute('InputAndPlay', source)
	
	def set_aux2(self):
		'''set the input source to aux2'''
		self.execute('Input','aux2')
	
	def set_cd(self):
		'''set the input source to cd'''
		self.execute('Input','cd')
	
	def set_tuner(self):
		'''set the input source to tuner'''
		self.execute('Input','tuner')
	
	def set_dvd(self):
		'''set the input source to dvd'''
		self.execute('Input','dvd')
		
	def set_game(self):
		'''set the input source to game'''
		self.execute('Input','game')
	
	def set_main_zone(self, arg='on'):
		''' Set the main zone on(defaut)/off'''
		self.execute('MainZone', arg)
	
	def set_sleep_timer(self, arg = 'on', value = 60):
		''' Set the sleep timer on(defaut)/off
			- value		:	delay in secondes (default = 60)
		'''
		if arg == 'off':
			value = None
		self.execute('SleepTimer', arg, value)


	