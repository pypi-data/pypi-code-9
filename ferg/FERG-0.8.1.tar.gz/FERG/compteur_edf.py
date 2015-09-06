#!/usr/bin/env python
# -*- coding:utf-8 -*

#Pour travailler sur les sources
import sys
sys.path.insert(0,'../../FGPIO')
sys.path.insert(0,'../../FUTIL')

from FGPIO.qrd1114_io import *
from FGPIO.mcp300x_hspi_io import *
from FGPIO.led_io import *
from FGPIO.bt_io import *

import time
import datetime
import logging

#TODO : créer start_record()
#		gestion HC/HP

class compteur_edf(object):
	'''Un compteur EDF avec une grosse roue qui tourne
		Sur lequel on va pouvoir calculer les consos a l'aide d'un capteur qrd1114 placé devant la roue
		qui va détecter le passage de la bande noire.
	'''
	timeout = 60		#Correspond à 150Watts
	time_pause = 0.001	#duree pause entre chaque mesure
	def __init__(self, capteur, capteur_hc = None, led = led_io(), intensity_max=45, energy_tr=2.5, nb_tours_mesure = 1, counter_hc = 0, counter_hp = 0):
		'''Initialisation
			- capteur			: 	qrd1114_io sur la roue
			- capteur_hc		:	qrd1114_io sur la fleche des heures creuses
			- intensite_max		:	intensité maximum de l'abonnement
			- energy_tr			:	energie par tour de roue en Wh/tr
			- led				:	led pour une impulsion par tour
			- nb_tours_mesure	:	Nb de tour de roue utilisés pour réaliser la mesure
		'''
		assert isinstance(capteur, qrd1114_analog_io), "capteur must be a qrd1114_analog_io"
		self.capteur = capteur
		assert capteur_hc == None or isinstance(capteur_hc, bt_io), "capteur_hc must be a bt_io"
		self.capteur_hc = capteur_hc
		assert isinstance(led, led_io), "led must be a led_io"
		self.led = led
		self.energy_tr = energy_tr
		self.mini_tr = 3600. / (intensity_max * 230)*self.energy_tr
		self.mini_noir = self.mini_tr *2.5/100*0.4 # durée mini du trait noir qui correspond à 2.5% du cercle -60% de marge
		self.nb_tours_mesure = nb_tours_mesure
		self.seuil_delestage = intensity_max * 230 * 0.90 # à 90% du max
		self.counter_hc = counter_hc
		self.counter_hp = counter_hp
		self.terminated = False #Pour tuer l'enregistrement
		
	
	def init_params(self):
		''' Calcul les paramètres de détection
		'''
		calculated = False
		while not calculated:
			logging.info("Mesure des paramètres du capteur......")
			self.led.blink(0.2)
			moyenne = 0
			maxi = 0
			nb = 0
			fin = time.time() + self.timeout
			while (maxi < moyenne * 5  or nb < 100) and time.time() < fin:
				value = self.capteur.read()
				moyenne = moyenne*nb+value
				nb+=1
				moyenne /= nb
				if value > maxi:
					maxi = value
					logging.debug("Voltage maxi : %s" % maxi)
				time.sleep(self.time_pause)
			self.voltage_moyen = moyenne
			self.gain_seuil = 1 + (maxi / moyenne - 1) * 0.50	# On se laisse une petite marge de 50%
			self.led.stop()
			if self.gain_seuil < 1.25:
				logging.warning("Seuil de detection de bande noire insuffisant.")
			else:
				logging.info( "Voltage_moyen : %.4f - Voltage maxi : %.4f - Seuil : %.4f"%(self.voltage_moyen, maxi, self.voltage_moyen*self.gain_seuil))
				calculated = True
	
	
	def init_record(self):
		'''Dois être lancée avant la première mesure
		'''
		self.init_params()
		self.wait_for_black()
	
	def record(self, rec_function):
		'''Boucle infinie pour mesures et enregistrement
			- rec_function		:		function qui va prendre les donnees en entrée
		'''
		logging.debug('compteur_edf.record() start.')
		_power = 0
		i = 0
		while i<self.nb_tours_mesure and not self.terminated:
			i+=1
			now = time.time()
			self.led.on()
			time.sleep(self.mini_tr/2)
			self.led.off()
			self.wait_for_black()
			duree = time.time() - now
			_power += self.energy_tr*3600/duree
		if not self.terminated:
			logging.debug('%s tour enregistres.' % self.nb_tours_mesure)
			# Mise à jours des compteurs (HC et HP)
			if self.type_horaire() == 'HC':
				self.counter_hc += self.energy_tr * self.nb_tours_mesure
				logging.info('Compteur HC = %s.' % self.counter_hc)
			else:
				self.counter_hp += self.energy_tr * self.nb_tours_mesure
				logging.info('Compteur HP = %s.' % self.counter_hp)
			# Enregistrement
			rec_function( \
					date_time=datetime.datetime.now(), \
					energy = self.energy_tr * self.nb_tours_mesure, \
					power = int(_power/self.nb_tours_mesure))
			
	
	def stop_record(self):
		'''Stop the record fonction
		'''
		self.terminated = True
	
	def wait_for_black(self):
		''' Attends que le voltage augmente jusqu'au voltage_seuil pendant au moins self.mini_noir ms
			Si ça dure trop longtemp, relance la mesure de la moyenne
		'''
		logging.debug('compteur_edf.wait_for_black().')
		timeout = time.time() + self.timeout
		black = False
		seuil=self.voltage_moyen*self.gain_seuil
		duree_noire = 0
		while not black:
			while duree_noire < self.mini_noir and time.time()<timeout:
				now=time.time()
				maximum_voltage = 0
				voltage = self.capteur.read()
				while voltage > seuil and time.time()<timeout:
					voltage = self.capteur.read() # temps de lecture du capteur < 0.0004 secondes
					maximum_voltage = max(maximum_voltage, voltage)
					time.sleep(self.time_pause/2)
				if maximum_voltage>0: # Pour gerer le cas ou le processeur fait autre chose!
					duree_noire = time.time()-now
					if duree_noire<self.mini_noir:
						logging.debug("Fausse bande noire : % secondes. Voltage maximum : %s" % (duree_noire, maximum_voltage))
				else:
					duree_noire = 0
				time.sleep(self.time_pause)
			if time.time()>timeout :
				logging.warning("Perte de la bande noire")
				self.init_params()
				timeout = time.time() + self.timeout
			else:
				black = True
				logging.debug("Durée de la bande noire : %s. Voltage maximum : %s" % (duree_noire, maximum_voltage))
	
				
	def mesure_moy(self, duration = 1):
		moyenne = 0
		nb = 0
		now=time.time()
		while time.time()<now+duration:
			moyenne += self.capteur.read()
			nb += 1
		return moyenne / nb
	
	def type_horaire(self):
		'''Renvoie le type d'horaire HC/HP
		'''
		if self.capteur_hc.read():
			return 'HC'
		else:
			return 'HP'

#########################################################
#                                                       #
#		EXEMPLE                                         #
#                                                       #
#########################################################

if __name__ == '__main__':
	pc = rpiduino_io()
	mcp3008 = mcp3008_hspi_io()	#Pour lecture analogique sur Rpi
	compteur = compteur_edf(qrd1114_analog_io(mcp3008.pin[0]), led_io(pc.bcm_pin(16)), 45,2.5)
	def rec_f(date_time, energy, power, counter):
			print "%s : %.1fWh ie %.1fWatts. Compteur : %s"%(date_time, energy, power, counter)
	compteur.record(rec_f)
	
	