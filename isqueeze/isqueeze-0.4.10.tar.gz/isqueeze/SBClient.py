#!/usr/bin/env python
# -*- coding:utf-8 -*


import time
import socket
import functools
import threading
#Pour SqueezeBox 
import server
import player
import logging
import unicodedata


class SBError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		logging.error(repr(self.value))
		return repr(self.value)


class SBClient:
	""" Classe decrivant un client SqueezeBox
		classe basée sur pylms"""
	def __init__(self, host="192.168.10.10", port = 9090, player="PISALON"):
		self.serveurSB = server.Server(hostname = host, port = port, charset = 'utf8')
		self.player=player
		self.lock = threading.RLock()
		logging.info("SBClient %s is created." % self)
		try:
			self.serveurSB.connect()
			self.clientSB = self.serveurSB.get_player(player)
		except socket.error:
			raise SBError("Connection au SqueezeServeur " + host +":" + str(port) + " impossible.")
	
	def update(self):
		'''Mise a jour de la connection au serveur'''
		logging.info('(Re)connection to %s' % self)
		try:
			self.serveurSB.connect()
			self.clientSB = self.serveurSB.get_player(self.player)
		except (EOFError, socket.error, ValueError), e:
			logging.error('Connection error to %s : %s' % (self, e))
	
	def unError(fonction):
		'''Decorateur pour 
			- eviter les erreurs
			- verouiller la connection à un seul thread
			- logger l'appel des fonctions
			
		Si erreur dans une des methodes, on essaye de reconnecter le serveur 1 fois
		Si ca ne passe toujours pas, on abandonne'''
		@functools.wraps(fonction) # ca sert pour avoir un help(SBClient) utile
		def DBUnErrorFonction(self,*args, **kwargs):
			with self.lock:
				logging.debug("%s execute : %s" % (self, fonction.__name__))
				try:
					return fonction(self,*args, **kwargs)
				except Exception, e:
					logging.warning(str(e) + ' in ' + fonction.__name__)
					logging.warning("Reconnection SqueezeServeur en cours ...")
					time.sleep(10)
					self.update()
					try:
						return fonction(self,*args, **kwargs)
					except Exception, e:
						logging.error('Reconnection SqueezeServeur failed. ' + str(e))
						return None
		return DBUnErrorFonction
		
	
	@unError
	def randomplay(self):
		""" lecture de la musique aleatoire sur toute la bibliotheque"""
		self.clientSB.randomplay()
	
	@unError
	def stop(self):
		""" stop la platine"""
		self.clientSB.stop()
	
	@unError
	def play(self):
		""" lecture de la musique stoppee"""
		self.clientSB.play()
	
	@unError
	def pause(self):
		"""pause de la musique"""
		self.clientSB.pause()
	
	@unError
	def next(self):
		"""morceau suivant"""
		self.clientSB.next()
	
	@unError
	def prev(self):
		"""morceau suivant"""
		self.clientSB.prev()
	
	@unError
	def synchronizeWithAll(self):
		""" Synchronize la platine avec toutes les autres"""
		clients = self.serveurSB.get_players()
		for client in clients:
			if client.ref!=self.clientSB.ref:
				client.sync_to(self.clientSB.ref)
	
	@unError
	def unsynchronize(self):
		"""De-synchronize la platine"""
		self.clientSB.unsync()
	
	@unError
	def unsynchronizeWithAll(self):
		""" De-Synchronise la platine avec toutes les autres"""
		clients = self.serveurSB.get_players()
		for client in clients:
			if client.ref!=self.clientSB.ref:
				client.unsync()
	
	@unError
	def get_mode(self, timeout = 30):
		"""Renvoie l etat de la platine"""
		fin = time.time() + timeout
		mode = self.clientSB.get_mode()
		while mode not in ('stop', 'play', 'pause') and time.time() < fin:
			logging.warning("Erreur in get_mode() commande. '%s' recu. Retry..." % mode)
			time.sleep(3)
			mode = self.clientSB.get_mode()
		if time.time() > fin:
			logging.error("Erreur in get_mode() commande. Timeout expire.")
		else:
			return mode
	
	@unError
	def get_track_title(self):
		""" renvoie le titre du morceau"""
		result = unicode(self.clientSB.get_track_title().strip())
		result = unicodedata.normalize('NFD', result).encode('ascii','ignore')
		return result
	
	@unError
	def get_track_artist(self):
		"""renvoie l artist"""
		result = unicode(self.clientSB.get_track_artist().strip())
		result = unicodedata.normalize('NFD', result).encode('ascii','ignore')
		return result
	
	@unError
	def get_track_album(self):
		""" Renvoie l album joue"""
		result = unicode(self.clientSB.get_track_album().strip())
		result = unicodedata.normalize('NFD', result).encode('ascii','ignore')
		return result
	
	@unError
	def SBplay(self):
		""" si pause, fait play(), sinon, fait randomplay()"""
		status = self.get_mode()
		if status=="pause":
			self.play()
		else:
			self.randomplay()
	
	@unError
	def on(self):
		""" Allume la platine"""
		self.clientSB.set_power_state(True)
		
	@unError
	def off(self):
		""" Etteint la platine"""
		self.clientSB.set_power_state(False)
	
	@unError
	def on_off(self):
		""" Si la platine est allumee, l etteint
		sinon l allume"""
		if self.clientSB.get_power_state():
			self.off()
		else:
			self.on()
			if self.get_mode() in ('stop', 'pause'):
				self.play()
	@unError
	def get_volume(self):
		""" Renvoie le volume de la platine
		"""
		return self.clientSB.get_volume()
		
	@unError
	def volume_down(self):
		""" Baisse le volume de la platine"""
		#TODO : passer en parametre une quantite de volume
		self.clientSB.volume_down()
	@unError
	def volume_up(self):
		""" Augmente le volume de la platine"""
		#TODO : passer en parametre une quantite de volume
		self.clientSB.volume_up()
	@unError
	def ir_button(self, action):
		""" Execute l'action passée en paramètre sur le serveur via ordre IR"""
		self.clientSB.ir_button(action)
		
	@unError
	def request_with_results(self, req):
		""" Execute une requete en telnet sur le serveur SqueezeBox
			Et renvoie (nb de resultat, liste des resultats, error ( False/True)
		"""
		return self.serveurSB.request_with_results(req)
	
	@unError
	def request(self, req):
		""" Execute une requete en telnet sur le serveur SqueezeBox
		"""
		self.serveurSB.request(req)
	
	@unError
	def search(self, term='', mode='artists', start = 0, max=None):
		""" Cherche dans la base de données du serveur
			et renvoie (nb_results, resultats, erreur)
				- term : recherche
				- mode : 'artists' | 'albums' | 'songs'
				- start : renvoie à partir du n°...
				- max  : nb maxi de retours
		"""
		if max==None:
			fin = False
			nb_results = 0
			resultats = []
			erreur = False
			while not fin:
				( the_nb_results, the_resultats, the_erreur) = self.search(term, mode, start, 50)
				nb_results+=the_nb_results
				resultats+=the_resultats
				erreur&=the_erreur
				if the_nb_results < 50:
					fin = True
				else:
					start = 50
			return (nb_results, resultats, erreur)
		else:
			if mode == 'albums':
				req = "albums %s %s tags:%s search:%s" % (start, max, "l", term)
			elif mode == 'songs':
				req = "songs %s %s tags:%s search:%s" % (start, max, "", term)
			elif mode == 'artists':
				req = "artists %s %s search:%s" % (start, max, term)
			return self.serveurSB.request_with_results(req)
	
	@unError
	def artists(self):
		"""Renvoie la liste des artists
		"""
		# On passe le premier qui correspond à "artistes divers"
		return self.serveurSB.request_with_results('artists')[1][1:]

	@unError
	def albums(self, artist_no = None):
		"""renvoie la liste des albums
			éventuellement limité à un artist (artist_no)
		"""
		if artist_no != None :
			return self.serveurSB.request_with_results('albums 0 50 artist_id:' + artist_no)[1]
		else:
			return self.serveurSB.request_with_results('albums search')[1]

	@unError
	def genres(self):
		"""Renvoie la liste des genres
		"""
		# On passe le premier qui correspond à rien (ou tout!)
		return self.serveurSB.request_with_results('genres search')[1][1:]
	
	@unError
	def radios(self):
		""" renvoie les types de radios
		"""
		#Mais en fait ca ne marche pas, la fonction request_with_results n'arrive pas
		# à parser le code renvoyer : à développer!!!!
		return self.serveurSB.request_with_results('radios 0 50')[1]
		
	@unError
	def favorites(self):
		""" Renvoie la liste des favories
		"""
		favorites = self.serveurSB.request_with_results('favorites items 0 50')[1]
		results = []
		# On enlève la premiere accurence (titre) ainsi que tous ce qui ne se joue pas
		for favorite in favorites[1:]:
			if favorite['isaudio'] != '0' and favorite['hasitems'] != '1':
				results.append(favorite)
		return results
	
	@unError
	def load_songs(self, genre = '*', artist = '*', album = '*'):
		""" Execute une requete sur le serveur : charge et joue une playliste 
			basée sur les critères :
				- genre
				- artist
				- album
		"""
		#On remplace les espaces par '%20' avant
		genre = genre.replace(' ','%20')
		artist = artist.replace(' ','%20')
		album = album.replace(' ','%20')
		self.clientSB.request('playlist loadalbum %s %s %s' % (genre, artist, album))
	
	@unError
	def play_favorite(self, id):
		"""Joue la radios, ou playliste favories
				-id	:	item_id
		"""
		self.clientSB.request('favorites playlist play item_id:%s' % (id))
	
	@unError
	def play_favorite_number(self, no):
		"""joue la radio ou playliste favorites
				-no	:	indice du favorie
		"""
		self.play_favorite(self.favorites()[no]['id'])
	
	@unError
	def rescan(self, mode='fast'):
		""" Rescan la bibliotheque du Serveur
			mode = 'fast' | 'full' | 'playlist'
		"""
		self.serveurSB.rescan(mode)
		
#########################################################
#                                                       #
#		EXEMPLE                                         #
#                                                       #
#########################################################

if __name__ == '__main__':
	maSB = SBClient("192.168.10.10", 9090, "PISALON")
	maSB.randomplay()