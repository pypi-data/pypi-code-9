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

import os
import json
import logging
import tornado.httpserver
import tornado.ioloop
import tornado.web 
import django.core.handlers.wsgi
import tornado.wsgi
from tornado import websocket
# django settings must be called before importing models

from zephserver.utils.roomhandler.roomhandler import RoomHandler
from zephserver.utils.decorator.sessiondecorator import Djangosession
from zephserver.infra.cluster_adapter import ClusterAdapter
from zephserversettings import PORT_ZEPH

from zephserver.infra.service_manager import ServiceManager
from zephserver.service.service_interface import ServiceInterface

class ClientSocketService(websocket.WebSocketHandler):
		
	def initialize(self):
		"""Store a reference to the "external" RoomHandler instance"""
		self._inmessage = {}
		self.__clientID = None
		self.__rh = ServiceManager.get_instance().get_service('zephserver.service.clientsocket_service/StartClientSocket').get_room_handler()
	
	def check_origin(self, origin):
		return True
	
	@Djangosession
	def on_message(self, user, message):
		self._inmessage = json.loads(message)
		if self.__clientID is None:
			self.__clientID = user.id

		self._inmessage["usersession"]= user
		if "task" in self._inmessage:
			self._inmessage["cid"]= self.__cid
			service_manager = ServiceManager.get_instance()
			routeur_service = service_manager.get_service('zephserver.service.routeur_service/RouteurService')
			routeur_service.route(self._inmessage)
		else:
			cid = self.__rh.add_roomuser(message, user)	
			self.__cid = cid
			self.__rh.add_client_wsconn(self.__cid, self)


	def open(self):
		#logging.info("WebSocket opened for %s" % user)
		pass
	 
	def on_close(self):
		self.__rh.remove_client(self.__cid)

				
settings = {
	"static_path": os.path.join(os.path.dirname(__file__), "static"),
	
	} 
# map the Urls to the class		  
wsgi_app = tornado.wsgi.WSGIContainer(django.core.handlers.wsgi.WSGIHandler())

class StartClientSocket(ServiceInterface):
	
	_room_handler = None
	_cluster = None
	
	def main(self):
		self._room_handler = RoomHandler()
		self._cluster = ClusterAdapter.get_instance()
		self._cluster.suscribe('clientsocket_send', self.say_cluster_callback)
		logging.info('launching ClientSocketService service')
		application = tornado.web.Application([
			(r"/", ClientSocketService),
			('.*', tornado.web.FallbackHandler, dict(fallback=wsgi_app)),
		], **settings)
		http_server = tornado.httpserver.HTTPServer(application)
		http_server.listen(PORT_ZEPH)
		tornado.ioloop.IOLoop.instance().start()
		logging.info('Tornado started')
	
	def get_room_handler(self):
		return self._room_handler
	
	def say(self, answer, from_cluster=False):
		if 'cid' not in answer and not from_cluster:
			self._cluster.send('clientsocket_send', answer)
		if 'room' in answer:
			self._room_handler.send_to_room(answer["room"], answer)
		elif 'users' in answer:
			self._room_handler.send_to_users(answer["users"], answer)
		elif 'all' in answer:
			self._room_handler.send_to_all( answer)
		elif 'cid' in answer:
			self._room_handler.send_to_cid(answer["cid"], answer)
	
	def say_cluster_callback(self, cluster_data):
		self.say(cluster_data['data'], True)
	
	def disable(self):
		logging.warning('asking to stop ClientSocketService service')
		tornado.ioloop.IOLoop.instance().stop()
		logging.info('Tornado stoped')
