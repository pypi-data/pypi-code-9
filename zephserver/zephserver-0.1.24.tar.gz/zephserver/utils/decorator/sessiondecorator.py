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


# django settings must be called before importing models
import django.conf
import django.contrib.auth
import django.utils.importlib
import logging
import json
from zephserver.infra.service_manager import ServiceManager

class DecorMethod(object):
	def __init__(self, decor, instance):
		self.decor = decor
		self.instance = instance

	def __call__(self, *args, **kw):
		return self.decor( self.instance, *args, **kw)

	def __getattr__(self, name):
		return getattr(self.decor, name)

	def __repr__(self):
		return '<bound method {} of {}>'.format(self.decor, type(self))
	
class Djangosession(object):

	def __init__(self, func):
		self.func = func
		
	def __get__(self, instance, owner):
		if instance is None:
			return self
		return DecorMethod(self, instance)

	def __call__(self, instance, *args, **kwargs):
		def closure(*args, **kwargs):
			user = self.get_current_user(instance, args)  
			return self.func(instance, user, *args, **kwargs)
		return closure(*args, **kwargs)
	
	def get_django_session(self, instance, message):
		message_content = json.loads(message[0])
		engine = django.utils.importlib.import_module(django.conf.settings.SESSION_ENGINE)
		try:
			session_key = message_content['session_id']
		except:
			pass
		self._session = engine.SessionStore(session_key)
		return self._session

	@staticmethod
	def get_django_dummy_session(instance):
		engine = django.utils.importlib.import_module(django.conf.settings.SESSION_ENGINE)
		session = engine.SessionStore(instance)
		return session

	  
	def get_current_user(self, instance, message):
		# get_user needs a django request object, but only looks at the session
		class Dummy(object): pass
		django_request = Dummy()

		try:
			#on essaye de se recuperer la session
			django_request.session = self.get_django_session(instance, message)
			user = django.contrib.auth.get_user(django_request)
		except:
			# en cas d'echec on reset la connexion a la db
			logging.info('db connection failed, trying reseting db')
			sm = ServiceManager.get_instance()
			db_service = sm.get_service('zephserver.service.db_service/DbService')
			db_service.reset_db()
			#on refait la requete
			django_request.session = self.get_django_session(instance, message)
			user = django.contrib.auth.get_user(django_request)

		
		try: 
			if user.is_authenticated():
				return user
			else:
				# try basic auth
				if not self.request.headers.has_key('Authorization'):
					return None
				kind, data = self.request.headers['Authorization'].split(' ')
				if kind != 'Basic':
					return None
				(username, _, password) = data.decode('base64').partition(':')
				user = django.contrib.auth.authenticate(username = username,
														password = password)
				if user is not None and user.is_authenticated():
					return user
				return None
		except Exception, e:
			logging.warning("authentification failed %s with exception %s" % (user, e))
