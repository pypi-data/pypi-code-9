# -*- coding: utf-8 -*-
'''
Copyright 2015 
	Centre de données socio-politiques (CDSP)
	Fondation nationale des sciences politiques (FNSP)
	Centre national de la recherche scientifique (CNRS)
License
	This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>
'''


from threading import Event
import logging
from django.db import connection

from zephserver.service.service_interface import ServiceInterface

class DbService(ServiceInterface):
	'''
		service gerant l'acces a la base de donnee et le cycle de vie des connexions a la bdd
		(pour l'instant il delegue a django)
	'''
	
	_shutdown_event = Event()

	def __init__(self):
		logging.info('instanciating db service')

	def main(self):
		logging.info('launching db service')
		self._shutdown_event.wait()
		self._shutdown_event.clear()

	def reset_db(self):
		from django import db
		logging.info('closing db')
		db.close_connection()

	def disable(self):
		logging.warning('asking to stop db service')
		self._shutdown_event.set()
		logging.info('db service stoped')

	def get_cursor(self):
		return connection.cursor()

		