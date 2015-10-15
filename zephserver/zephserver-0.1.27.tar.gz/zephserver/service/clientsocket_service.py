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

import os, sys
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
from zephserversettings import PORT_ZEPH, MY_ROOM_HANDLER, MY_SESSION_HANDLER

from zephserver.infra.service_manager import ServiceManager
from zephserver.service.service_interface import ServiceInterface
try:
    from zephserversettings import DJANGO
except: 
    from zephserver.settings import DJANGO

class ClientSocketService(websocket.WebSocketHandler):
		
	def initialize(self):
		"""Store a reference to the "external" RoomHandler instance"""
		self._inmessage = {}
		self.__clientID = None
		self.__user = None
		self.__rh = ServiceManager.get_instance().get_service(MY_ROOM_HANDLER)
		self.__session = ServiceManager.get_instance().get_service(MY_SESSION_HANDLER)
	
	def check_origin(self, origin):
		return True
	
	def on_message(self, message):
		self.get_user(message)
		self._inmessage = json.loads(message)
		if self.__clientID is None:
			self.__clientID = self.__user.id
		logging.info(message)
		self._inmessage["usersession"]= self.__user
		if "task" in self._inmessage:
			self._inmessage["cid"]= self.__cid
			service_manager = ServiceManager.get_instance()
			routeur_service = service_manager.get_service('zephserver.service.routeur_service/RouteurService')
			routeur_service.route(self._inmessage)
		else:
			logging.info(message)
			cid = self.__rh.add_roomuser(message, self.__user)	
			self.__cid = cid
			self.__rh.add_client_wsconn(self.__cid, self)


	def open(self):
		#logging.info("WebSocket opened for %s" % user)
		pass
	 
	def on_close(self):
		self.__rh.remove_client(self.__cid)

	def get_user(self, message):			
		if DJANGO:
			self.__user = self.__session.get_current_user(self, message)
		else:
			mess = json.loads(message)
			logging.info(mess)
			class Dummy(object): pass
			self.__user = Dummy()
			self.__user.id = mess['session_id']['id']
			self.__user.username = mess['session_id']['username']
			
settings = {
	"static_path": os.path.join(os.path.dirname(__file__), "static"),
	
	} 
# map the Urls to the class		  
wsgi_app = tornado.wsgi.WSGIContainer(django.core.handlers.wsgi.WSGIHandler())

class StartClientSocket(ServiceInterface):
	
	_room_handler = None
	_cluster = None
	
	def main(self):
		self._room_handler = ServiceManager.get_instance().get_service(MY_ROOM_HANDLER)
		self._cluster = ClusterAdapter.get_instance()
		self._cluster.subscribe('clientsocket_send', self.say_cluster_callback)
		logging.info('launching ClientSocketService service')
		application = tornado.web.Application([
			(r"/", ClientSocketService),
			('.*', tornado.web.FallbackHandler, dict(fallback=wsgi_app)),
		], **settings)
		http_server = tornado.httpserver.HTTPServer(application)
		http_server.listen(PORT_ZEPH)
		tornado.ioloop.IOLoop.instance().start()
		logging.info('Tornado started')
	
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
