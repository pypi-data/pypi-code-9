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


import logging, importlib
from threading import Lock, Thread
from zephserversettings import SERVICE_LIST


class ServiceManager(object):
	'''
		@sigleton
		class managing the services and their lifecycles.
		due to some locks protecting memory this class can be 
		a bottleneck if you want to manage a lot of services 
		in a small time

		A service lifecycle is inspired from Apache. It is first available then it can be enabled

		If a service crash the servicemanager will ytry to relaunch it (same object) in an other thread
	'''

	_instance = None
	_instance_lock = Lock()

	_manipulating_service_lock = Lock()

	_services_available = {}
	_services_enable = {}

	_pending_stop = False


	def __init__(self):
		'''
			private constructor, do not use
		'''
		logging.info('instatiating service_manager')
		pass


	@classmethod
	def get_instance(cls):
		'''
			singleton management
		'''
		if not cls._instance:
			cls._instance_lock.acquire()
			try:
				if not cls._instance:
					cls._instance = ServiceManager()
			finally:
				cls._instance_lock.release()
		return cls._instance

	
	def enable_service(self, service_name):
		'''
			Method enabeling a service whitch is already avaiable

			Enabeling a service means launching its thread (calling its main method)

			this method return True if the service has been enabled and False otherwise
		'''
		if self._services_available.has_key(service_name) and not self._services_enable.has_key(service_name) and self._pending_stop == False:
			self._manipulating_service_lock.acquire()
			try:
				if self._services_available.has_key(service_name) and not self._services_enable.has_key(service_name) and self._pending_stop == False:
					logging.debug('enabeling service %s', service_name)
					service = self._services_available[service_name]
					service.get_service_lock().acquire()
					if service.has_run():
						service.restart()
					else:
						service.start()
					service.get_service_lock().acquire()
			finally:
				service.get_service_lock().release()
				self._manipulating_service_lock.release()
				return True
		else:
			logging.warning('fail enabeling service %s', service_name)
			return False
			


	def enable_all_services(self):
		'''
			Method enabeling all services available
		'''
		logging.debug('enabelling all services')
		output = True
		for service in self._services_available:
			if not self.enable_service(service):
				output = False
		logging.debug('enabelling all servicies... done')
		return output


	def disable_service(self, service_name):
		'''
			function disableing (killing threads) all services enabled
		'''
		logging.debug('disabelling %s', service_name)
		service = self._services_enable.get(service_name, None)
		if not service == None:
			service.disable()
			service.join()
			logging.debug('disabelling %s done', service_name)
			return True	
		else:
			logging.warning('disabelling %s fail', service_name)
			return False


	def disable_all_services(self):
		'''
			Fonction desactivant tout les services
			fonction retourne True si tout les services ont ete lance et false sinon
		'''
		logging.debug('disabelling all services')
		output = True
		services = self._services_enable.copy()
		for service in services:
			if not self.disable_service(service):
				output = False
		logging.debug('disabelling all services... done')
		return output



	def create_service(self, service_name, service_instance):
		'''
			Fonction inscrivant un service parmis ceux disponibles pour etre demare
			la function retourne True si on l'a inscrit et False sinon
		'''
		logging.debug('creating %s', service_name)
		if not self._services_available.has_key(service_name):
			self._manipulating_service_lock.acquire()
			if not self._services_available.has_key(service_name):
				self._services_available[service_name] = ServiceContainer(service_name,service_instance)
			self._manipulating_service_lock.release()
			logging.debug('creating %s ... done', service_name)
			return True
		else:
			logging.warning('creating %s ... fail', service_name)
			return False

	def create_all_service(self, enable_all=False):
		'''
			méthode instatiant dynamiquement tout les services presant dans 
			la variable services_liste de configs.py
		'''
		logging.info('instanciating all services')
		for path in SERVICE_LIST:
			logging.debug('importing service : %s', path)
			module = importlib.import_module(path.split('/')[0])
			class_def = getattr(module, path.split('/')[-1])()
			self.create_service(path, class_def)
		if enable_all:
			self.enable_all_services()

	def delete_service(self, service_name):
		'''
			fonction desinscrivant un service le rendant innacessible
			la fonction retourne True si le service est trouve et desinscrit et False sinon
		'''
		logging.debug('deleting %s', service_name)
		if self._services_available.has_key(service_name):
			self._manipulating_service_lock.acquire()
			if self._services_available.has_key(service_name):
				del self._services_available[service_name]
			self._manipulating_service_lock.release()
			logging.debug('deleting %s ... done', service_name)
			return True
		else:
			logging.warning('deleting %s ... fail', service_name)
			return False


	def delete_all_services(self):
		'''
			Fonction detruisant tout les services
			fonction retourne True si tout les services ont ete detruits et false sinon
		'''
		logging.debug('deleting all services')
		output = True
		services = self._services_available.copy()
		for service in services:
			if not self.delete_service(service):
				output = False
		logging.debug('deleting all services...done')
		return output


	def get_service(self, service_name):
		'''
			Fonction retournant le service demande si il existe et le lançant si besoin
			la fonction retourne None si le service n'est pas trouve
		'''
		logging.debug('getting service %s',service_name)
		if self._services_enable.has_key(service_name):
			return self._services_enable[service_name].get_service()
		elif self._pending_stop == True:
			logging.warning('service %s not found and stop pendding',service_name)
			return None
		elif self._services_available.has_key(service_name):
			if not self.enable_service(service_name):
				logging.warning('service %s found but disable',service_name)
				return None
			return self._services_enable[service_name].get_service()
		else:
			logging.warning('service %s not found !', service_name)
			return None

	def stop_service_manager(self):
		'''
			Fonction éteignant proprement les services
		'''
		logging.info('Stopping service_manager')
		self._pending_stop = True
		self.disable_all_services()
		self.delete_all_services()
		self._instance_lock.acquire()
		self._instance = None
		self._instance_lock.release()
		self._pending_stop = False
		logging.info('servicemanager stopped')



class ServiceContainer(Thread):
	'''
		calsse privé permetant de gérer plus finement les cycle de vie en se recréant pour relancé un service éteint.
	'''
	_service_name = ''
	_service_instance = ''
	_service_lock = Lock()
	_has_run = False

	def __init__(self,service_name, service_instance):
		Thread.__init__(self)
		self._service_instance = service_instance
		self._service_name = service_name
		

	def run(self):
		ServiceManager.get_instance()._services_enable[self._service_name] = self
		self._service_lock.release()
		logging.debug('success enabeling service %s', self._service_name)
		try:
			self._service_instance.main()
		finally:
			self._has_run = True
			ServiceManager.get_instance()._manipulating_service_lock.acquire()
			try:
				del ServiceManager.get_instance()._services_enable[self._service_name]
			finally:
				ServiceManager.get_instance()._manipulating_service_lock.release()

	def disable(self):
		'''
			transmet le signal de mort
		'''
		self._service_instance.disable()

	def get_service_lock(self):
		'''
			access the lock of the this ServiceContainer
		'''
		return self._service_lock


	def get_service(self):
		'''
			interace pour être transparent hors du gestionnaire de services
		'''
		return self._service_instance

	def has_run(self):
		'''
			encapsumation de la variable self._has_run
		'''
		return self._has_run

	def restart(self):
		'''
			methode permetant de contourner la  limitation a un démarage par 
			thread en recréant un thread si un demarage est demandé et que le 
			thread a deja été demaré une fois

			cette methode est tres prive et ne doit être apelle qua dans la 
			fonction de démarage de service ServiceManager.enable_service sous
			peine de comportements non définis
		'''
		#_services_available
		service_manager = ServiceManager.get_instance()

		if service_manager._services_available.has_key(self._service_name):
			del service_manager._services_available[self._service_name]
		if service_manager._services_enable.has_key(self._service_name):
			del service_manager._services_enable[self._service_name]

		service_manager.create_service(self._service_name, self._service_instance)
		service_manager.enable_service(self._service_name)
		self._service_lock.release()
		