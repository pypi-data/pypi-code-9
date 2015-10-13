#!/usr/bin/env python
# -*- coding:utf-8 -*


# ---------------------------------------------------------------------
#    
#	Interface pour squeezeBox sur Rasberry Pi ou pcduino
#	
#	basée sur FGPIO : lib pour gestion GPIO rpiduino (=Rpi ou pcduino)
#	
#	Fonctions :
#					-	Boutons on_off, suivant, pause
#					-	Boutons presets
#					-	LCD
#					-	Navigation menu via bouton rotatif
#					-	télécommande Infra Rouge
#					-	communication avec Ampli Home cinéma (Denon)
#	
# ----------------------------------------------------------------------

import sys
sys.path.insert(0,'../../FGPIO')#Pour travailler sur les sources
sys.path.insert(0,'../../FAVRIP')

from SBClient import *
from FGPIO.led_io import *
from FGPIO.f_thread import *
from FGPIO.f_menu import *
import time
import logging

try:
	import pylirc # Pour InfraRouge
except:
	logging.error('Importation pylirc a echoué!')
	pass

#TODO : gerer les paramètres None (ecran, bt_rot, ...)


class isqueeze(object):
	'''Une interface pour squeezebox
	'''
	def __init__(self, \
					SB_serveur_ip, SB_client_name, \
					bt_onoff, bt_playpause, bt_next, \
					SB_serveur_port = 9090, \
					ampli = None, ampli_input = None, \
					lcd = None, led = None,	\
					bt_rot = None, bts_preset = [], \
					infra_rouge = False):
		'''Initialisation de l'interface
			- SB_serveur_ip		:	squeezebox serveur ip adress (ex : '192.168.0.5')
			- SB_client_name	:	squeezeBox client name
			- SB_serveur_port	:	squeezeBox serveur port (default=9090)
			- ampli				:	home cimena ampli (FAVRIP.favrip object)
			- lcd				:	lcd display (FGPIO.lcd_io object)
			- led				:	on_off led (FGPIO.led_io object)
			- bt_onoff			:	on_off button (FGPIO.bt_io object)
			- bt_playpause		:	playpause button (FGPIO.bt_io object)
			- bt_next			:	next button (FGPIO.bt_io object)
			- bt_rot			:	rotary button for menu (FGPIO.rotary_encoder_io object)
			- bts_preset		:	list of preset button (list of FGPIO.bt_io objects)
			- infra_rouge		:	True if infra_rouge is enabled
		'''
		self.SB = SBClient(SB_serveur_ip, SB_serveur_port, SB_client_name)
		self.ampli = ampli
		self.ampli_input = ampli_input
		self.lcd = lcd
		if led == None:
			self.led = led_io()
		else:
			self.led = led
		self.bt_onoff = bt_onoff
		self.bt_playpause = bt_playpause
		self.bt_next = bt_next
		self.bt_rot = bt_rot
		self.bts_preset = bts_preset
		self.infra_rouge = infra_rouge
		
		# Initialisation de l'état de l'interface
		self.status = self.SB.get_mode()
		self.menu_on = False
		self.ampli_status = {'ampli' : self.get_ampli_status(), 'sb' : self.status}
		
		# Création du menu
		menu = f_menu( \
			f_item("Lecture aleatoire", f_cmd(self.lecture_aleatoire)), \
			f_item("Ma musique", f_menu( \
				f_item("Artist", f_menu_dynamic(self.artists, 'play')), \
				f_item("Album", f_menu( \
					f_item("par Artist", f_menu_dynamic(self.artists, 'albums')), \
					f_item("par Nom Album",f_menu_dynamic(self.albums)))), \
				f_item("Genre", f_menu_dynamic(self.genres)) \
				)), \
			f_item("Synchronisation", f_menu( \
				f_item("Sync. toutes", f_cmd(self.SB.synchronizeWithAll)), \
				f_item("Desync. toutes", f_cmd(self.SB.unsynchronizeWithAll)), \
				f_item("Desync. PISALON", f_cmd(self.SB.unsynchronize)))), \
			f_item("Radios Favories", f_menu_dynamic(self.favorites)), \
			f_item("Shutdown", f_cmd(self.shutdown)), \
			f_item("Exit", None)
			)
		
		self.menu = f_interface(self.lcd, self.bt_rot, menu, 15, 0.2)
		
		#Mise en fonction des deamons liés au buttons
		self.bt_onoff.add_thread(self.on_bt_onoff, pause=0.25)
		self.bt_playpause.add_thread(self.on_bt_playpause, pause = 0.25)
		self.bt_next.add_thread(self.on_bt_next, pause = 0.25)
		#Création des méthodes on_bt_preset pour chaque bouton preset
		for i, bt_preset in enumerate(self.bts_preset):
			self._add_methode_on_bt_preset(i)
			bt_preset.add_thread(getattr(self, 'on_bt_preset_%d' % i), pause = 0.25)
		self.bt_rot.add_thread(on_rot_changed = self.on_bt_volume, rot_pause = 0.25)
		#Mise en fonction du deamon scroll
		#self.lcd.add_scroll_thread() Inutil!
		
		#Autres deamons
		
		#Lecture état serveur squeezeBox et affichage lcd
		self.th_squeeze_to_isqueeze = f_thread(self.squeeze_to_isqueeze)
		self.th_squeeze_to_isqueeze.start()
		#Attente push button et entrée dans menu
		self.th_menu = f_thread(self.to_menu)
		self.th_menu.start()
		#Gestion des liens avec ampli
		self.th_check_ampli = f_thread(self.check_ampli)
		self.th_check_ampli.start()
		#Reboot manager pour éviter que ça plante (bug squeezeplug)
		self.th_reboot_manager = f_thread(self.reboot_manager)
		self.th_reboot_manager.start()
		
		# Initialisation de l'Infra rouge
		if self.infra_rouge:
			self.th_telecommande = f_thread(self.telecommande)
			self.th_telecommande.start()
			erreur = True
			end_time = time.time()+60
			while erreur and time.time()<end_time:
				try:
					sockid = pylirc.init("SqueezeCmdIR")
					pylirc.blocking(False)
					erreur = False
				except:
					time.sleep(15)
		if erreur:
			logging.error("Infra rouge fail to initialise : timeout")
		else:
			logging.info("Infra rouge :OK")
		logging.info("isqueeze initialized : %s" % self)
	
	#########################################
	#										#
	#			FONCTIONS GENERALES			#
	#										#
	#########################################
	
	def wait_ctrl_c(self):
		''' Attend juste un CTRL-C pour tout stopper'''
		try:
			while True:
				time.sleep(2)
		except KeyboardInterrupt:
			self.stop()
	
	def stop(self):
		'''Stoppe les deamons'''
		if self.infra_rouge:
			self.th_telecommande.stop()
		self.th_squeeze_to_isqueeze.stop()
		self.th_menu.stop()
		#self.th_volume.stop()
		for bt in self.bts_preset:
			bt.stop()
		self.bt_onoff.stop()
		self.bt_playpause.stop()
		self.bt_next.stop()
		self.th_check_ampli.stop()
		self.bt_rot.stop()
		self.lcd.stop()
		self.th_reboot_manager.stop()
	
	def shutdown(self):
		'''Restart the system
		'''
		logging.info("isqueeze stop the system!!!")
		command = "/usr/bin/sudo /sbin/shutdown -r now"
		import subprocess
		process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
	
	#########################################
	#										#
	#			FONCTIONS DU MENU			#
	#										#
	#########################################
	
	def lecture_aleatoire(self):
		logging.info("isqueeze : lecture_aleatoire")
		self.SB.randomplay()
		self.lcd.message("Initialisation liste aleatoire")
		time.sleep(1)
	
	def artists(self, mode):
		logging.info("isqueeze : artists %s" % mode)
		artists = self.SB.artists()
		if artists==None: # Si ca ne marche pas, on reessaye!!!
			logging.warning("error on SB.artists(). Retry once.")
			time.sleep(2)
			artists = self.SB.artists()
		menu_items = []
		if artists!=None:
			for artist in artists:	
				logging.debug("Artist found : %s" % artist)
				if mode == 'play':
					menu_items.append(f_item(artist['artist'],f_cmd(self.play_artist, artist['artist'])))
				if mode == 'albums':
					menu_items.append(f_item(artist['artist'],f_menu_dynamic(self.albums, artist['id'])))
		return menu_items
	
	def albums(self, artist_no=None):
		logging.info("isqueeze : albums %s" % artist_no)
		albums = self.SB.albums(artist_no)
		if albums==None: # Si ca ne marche pas, on reessaye!!!
			logging.warning("error on SB.albums(). Retry once.")
			time.sleep(2)
			albums = self.SB.albums(artist_no)
		menu_items = []
		if albums!=None:
			for album in albums:
					logging.debug("Album found : %s" % album)
					menu_items.append(f_item(album['album'],f_cmd(self.play_album, album['album'])))
		return menu_items	
	
	def genres(self):
		logging.info("isqueeze : genre")
		genres = self.SB.genres()
		if genres==None: # Si ca ne marche pas, on reessaye!!!
			logging.warning("error on SB.genres(). Retry once.")
			time.sleep(2)
			genres = self.SB.genres()
		menu_items = []
		if genres!=None:
			for genre in genres:
				logging.debug("Genre found : %s" % genre)
				menu_items.append(f_item(genre['genre'],f_cmd(self.play_genre, genre['genre'])))
		return menu_items
	
	def favorites(self):
		logging.info("isqueeze : favorite")
		favorites = self.SB.favorites()
		if favorites==None:# Si ca ne marche pas, on reessaye!!!
			logging.warning("error on SB.favorite(). Retry once.")
			time.sleep(2)
			favorites = self.SB.favorites()
		menu_items = []
		if favorites!=None:
			for favorite in favorites:
				logging.debug("Favorite found : %s" % favorite)
				menu_items.append(f_item(favorite['name'],f_cmd(self.play_favorite, favorite['id'])))
		return menu_items
		
	def play_artist(self, nom_artist):
		logging.info("isqueeze : play_artist")
		self.SB.load_songs(artist = nom_artist) 
	
	def play_album(self, nom_album):
		logging.info("isqueeze : play_album")
		self.SB.load_songs(album = nom_album)
	
	def play_genre(self, nom_genre):
		logging.info("isqueeze : play_genre")
		self.SB.load_songs(genre = nom_genre)
	
	def play_favorite(self, id):
		logging.info("isqueeze : play_favorite")
		self.SB.play_favorite(id)
		
	def recherche_radio(self):
		"""On va rechercher les radios comme dans une squeezebox
			- Notre selection/Local/Musique/....
		"""
		logging.info("isqueeze : recherche_radio")
		radios = self.SB.radios() # En fait ça ne marhce pas!!!
		logging.error("Ca ne fonctionne pas : à coder!!!")
		return []
		
	def recherche(self):
		logging.info("isqueeze : recherche")
		logging.error("Ca ne fonctionne pas : à coder!!!")
	
	def set_radio(self, radio): #Ou alors voir avec les preset
		logging.info("isqueeze : set_radio")
		logging.error("Ca ne fonctionne pas : à coder!!!")
	
	#########################################
	#										#
	#			THREADS						#
	#										#
	#########################################
	def squeeze_to_isqueeze(self):
		'''Lecture de l'état de la squezebox et mise à jour de l'affichage et led
		'''
		if not self.menu_on:
			try:
				status = self.SB.get_mode() # Lecture du status de la squeezeBox
			except:
				logging.warning("isqueeze : serveur inaccessible")
				status = None
			# Si le serveur est inaccessible
			if status==None:
				if not self.status==None:
					logging.error('Lecture status : pas de réponse')
					self.lcd.message('Erreur : pas de reponse du serveur squeezebox')
			else:
				if self.status==None:
					pass
					logging.error('Lecture status : connection retrouvée')
			self.status = status
			if self.status!="stop" and self.status != None:
				#lecture du nom de la musique en cours
				try:
					track = self.SB.get_track_title()
				except:
					logging.warning("Error reading track_title from SqueezeBoxServeur.")
					track = ""
				if self.status=='pause':
					message='<pause>'
				else:
					message=''
				if track!=None:
					if message=='':
						message=track
					else:
						message+=' ' + track
				try:
					artist = self.SB.get_track_artist()
				except:
					logging.warning("Error reading track_artist from SqueezeBoxServeur.")
					artist = ''
				if artist!=None:
					if message=='':
						message=artist
					else:
						message+=' - ' + artist
				try:
					album = self.SB.get_track_album()
				except:
					logging.warning("Error reading track_album from SqueezeBoxServeur.")
					album = ''
				if album!=None:
					if message=='':
						message=album
					else:
						message+=' - ' + album
				self.lcd.message(message, False, True)
				logging.debug(str(track) + ' - ' + str(album) + ' - ' + str(artist))
			if status=="stop":
				self.lcd.message("SqueezeBox PISALON stoppee")
				self.lcd.backlight(False) # éteindre l ecran
			else:
				self.lcd.backlight(True)
			# Mise a jour de l'etat de la led
			if status=="play":
				self.led.on()
			else:
				self.led.off()
		time.sleep(1)
	
	def on_bt_onoff(self):
		''' Deamon quand le bouton on_off change d'état
		'''
		if self.bt_onoff.th_readed():
			status = self.SB.get_mode() # on récupère le status de la squeezeBox
			logging.debug('bt_onoff is pressed')
			if status=="stop":
				self.SB.randomplay()
				self.led.on()
				status="play"
				logging.debug('randomplay')
			else:
				self.SB.stop()
				self.led.off()
				status="stop"
				logging.debug('stop')
	
	def on_bt_playpause(self):
		'''Deamon quand le bouton play_pause change d'état
		'''
		if self.bt_playpause.th_readed():
			status = self.SB.get_mode() # on récupère le status de la squeezeBox
			logging.debug('bt_playpause')
			if status=="play":
				self.SB.pause()
				self.led.off()
				status="pause"
				logging.debug('pause')
			else:
				self.SB.play()
				self.led.on()
				status="play"
				logging.debug('play')	
	
	def on_bt_next(self):
		'''Deamon quand le bouton next change d'état
		'''
		if self.bt_next.th_readed():
			logging.debug('bt_suivant')
			self.SB.next()
			self.led.on()
			logging.debug('next')
	
	def on_bt_preset(self, no_bt):
		'''Deamon quand bouton preset change d'état
		'''
		if self.bts_preset[no_bt].th_readed():
			logging.debug('bt_preset_%s is pushed : play_favorite()' % no_bt)
			self.SB.play_favorite_number(no_bt)
	
	def _add_methode_on_bt_preset(self, i):
		'''Pour création des méthodes
			on_bt_preset_0
			on_bt_preset_1
			...
		'''
		def on_bt_preset_i(self):
			self.on_bt_preset(i)
		on_bt_preset_i.__name__ = 'on_bt_preset_%d' % i
		setattr(self.__class__, on_bt_preset_i.__name__, on_bt_preset_i)	
	
	def to_menu(self):
		"""Gestion du menu
		"""
		# On entre dans le menu en apuyant sur le bouton
		if self.bt_rot.is_pushed():
			self.menu_on = True
			time.sleep(0.5)#Pour être sur que le thread squeeze_to_isqueeze a bien terminé ses affichages
			self.menu.start()
			self.menu_on = False
		time.sleep(0.2)
	
	def on_bt_volume(self):
		""" réglage du volume par bouton rotatif
			quand pas menu
		"""
		#TODO : affichage sur lcd du volume sur derniere ligne
		if not self.menu_on:
			if self.bt_rot.th_readed() == 1:
				self.SB.volume_up()
			if self.bt_rot.th_readed() == -1:
				self.SB.volume_down()
		#else:
		#	time.sleep(1)
	
	def telecommande(self):
		""" 
			Lecture capteur Infra Rouge    
		et envoie commande telnet sur squeezeserver 
		(configuration : 
			/etc/modules : lancement lirc sur port GPIO_18
			/etc/lirc/hardware.conf : params generaux
			/etc/lirc/lircd.conf : params telecommande
			/etc/lirc/lircrc : les touches et les commandes http
		"""
		code = pylirc.nextcode() 
		if code:
			exec("self.SB." + code[0])
			logging.info("Telecommande : " + code[0])
		time.sleep(0.3)
	
	def get_ampli_status(self):
		'''Renvoie True si l'ampli est en ecoute sur la squeezeBox
		'''
		if self.ampli.get_power()=='on':
			return self.ampli.get_input() == self.ampli_input
		else:
			return False
	
	def check_ampli(self):
		'''Gère les relations avec l'ampli
			- Si la squeezeBox devient allumé, on allume aussi l'ampli
			- Si la squeezeBox devient stoppée, on eteint l'ampli s'il est bien sur l'input de isqueeze
			- Si l'ampli devient eteint, on stoppe la squeezebox
			- Si l'ampli devient allumé sur l'input de isqueeze, on allume si besoin le squeezebox
		'''
		if self.ampli!=None:
			ampli_status = {'ampli' : self.get_ampli_status(), 'sb' : self.SB.get_mode()}
			if self.ampli_status['sb']=='play' and ampli_status['sb']=='stop':
				if ampli_status['ampli']:
					logging.info("Ampli set off by squeezebox (play => stop)")
					self.ampli.off()
			elif self.ampli_status['sb']=='stop' and ampli_status['sb']=='play':
				if not ampli_status['ampli']:
					logging.info("Ampli set on by squeezebox (stop => play)")
					self.ampli.on()
					self.ampli.set_input(self.ampli_input)
			elif self.ampli_status['ampli'] and not ampli_status['ampli']:
				if ampli_status['sb']!='stop':
					logging.info("SqueezeBox NOT set off by ampli.")
					self.SB.stop()
			elif not self.ampli_status['ampli'] and ampli_status['ampli']:
				if ampli_status['sb']!='play':
					logging.info("SqueezeBox NOT set on by ampli.") 
					self.SB.play()
			self.ampli_status = ampli_status
		time.sleep(5)
	
	def reboot_manager(self, duration = 21600): #par defaut toutes les 6 heures
		'''Reboot le systeme de temps en temps quand la squeezeBox est sur stop
		'''
		end = time.time() + duration
		while time.time() < end:
			time.sleep(duration / 10)
		while self.status != 'stop':
			time.sleep(duration / 10)
		self.shutdown()
		
	

#########################################################
#                                                       #
#		EXEMPLE de MAIN	                                #
#                                                       #
#########################################################


if __name__ == '__main__':
	
	from FAVRIP.denon import *
	from FGPIO.rpiduino_io import *
	from FGPIO.lcd_i2c_io import *
	from FGPIO.bt_io import *
	from FGPIO.rotary_encoder_io import *
	from FUTIL.my_logging import *
	my_logging(console_level = DEBUG, logfile_level = INFO)
	
	pc = rpiduino_io()
	
	if isinstance(pc, pcduino_io): # Si c'est un pcduino
		lcd = lcd_i2c_io(bus=2,addr=0x27, pin_bl=pc.logical_pin(6), lines=2, width=16)
		#led = led_io(pc.logical_pin(2)) # led sur pin 2 arduino ou 13 Rpi (GPIO2)
		bt_onoff = bt_io(pc.logical_pin(3))# Bt on_off sur la pin 3 arduino ou GPIO3 du Rpi
		bt_playpause = bt_io(pc.logical_pin(4))
		bt_next = bt_io(pc.logical_pin(5))
		#bt_rot = bt_rotatif_io(*pc.logical_pins(9,10,8), auto=True)
		bt_rot = bt_pseudo_rotatif_io(*pc.logical_pins(10,9,8)) #pour test en émulant un bouton rotatif par 3 boutons
		ext_io = mcp23017_io(addr=0x23, pc=pc)
		bts_preset = [ \
			bt_io(ext_io.pin[8]), \
			bt_io(ext_io.pin[9]), \
			bt_io(ext_io.pin[10]), \
			bt_io(ext_io.pin[11]), \
			bt_io(ext_io.pin[12]), \
			bt_io(ext_io.pin[13]) \
			]
		infra_rouge = False
	else: # Si c'est un Raspberry Pi
		lcd = lcd_i2c_io(pc=pc, pin_bl=pc.physical_pin(8), lines=4, width=20)
		#led = led_io(pc.physical_pin(21)) # led sur pin 2 arduino ou 13 Rpi (GPIO2)
		bt_onoff = bt_io(pc.physical_pin(11)) # Bt on_off sur la pin 3 arduino ou GPIO3 du Rpi
		bt_playpause = bt_io(pc.physical_pin(13))
		bt_next = bt_io(pc.physical_pin(15))
		bt_rot = bt_rotatif_io(*pc.physical_pins(18,16,7), auto=True)
		bts_preset = [ \
			bt_io(pc.physical_pin(26)), \
			bt_io(pc.physical_pin(24)), \
			bt_io(pc.physical_pin(23)), \
			bt_io(pc.physical_pin(22)), \
			bt_io(pc.physical_pin(21)), \
			bt_io(pc.physical_pin(19)) \
			]
		infra_rouge = True
	
	myisqueeze = isqueeze( \
					SB_serveur_ip = '192.168.10.10', \
					SB_client_name = 'PISALON', \
					ampli = denonAVR('192.168.10.11'), \
					ampli_input = 'aux2',\
					lcd = lcd, \
					bt_onoff = bt_onoff, \
					bt_playpause = bt_playpause, \
					bt_next = bt_next, \
					bt_rot = bt_rot, \
					bts_preset = bts_preset, \
					infra_rouge = infra_rouge)
	
	myisqueeze.wait_ctrl_c()