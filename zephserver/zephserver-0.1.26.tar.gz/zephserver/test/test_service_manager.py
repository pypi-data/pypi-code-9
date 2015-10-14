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


import unittest
import sys, os
path = ("/").join( sys.path[0].split("/")[:-2] )
print path
if path not in sys.path:
    sys.path.append(path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'djangoproject.settings'

from zephserver.infra.service_manager import ServiceManager
from zephserver.service.service_interface import ServiceInterface


class TestServiceManager(unittest.TestCase):
	'''
		ensemble des testes unitaires pour la classe servicemanager
	'''
	#instance du serveur
	_bootstrap = None
	
	def setUp(self):
		#avant chaque test on lance le serveur pour avoir un environnement propre	
		from django import setup
		setup()
		from zephserver.infra.bootstrap import Bootstrap
		self._bootstrap = Bootstrap()
		self._bootstrap._is_testing = True
		self._bootstrap.start_server()

	def tearDown(self):
		#apres chaque test on eteint le serveur
		service_manager = ServiceManager.get_instance()
		service_manager._services_available = {}
		service_manager._services_enable = {}
		service_manager._pending_stop = False
		


	#tests du sigleton
	def test_get_instance_simple(self):
		print('\ntest de la recuperation d\'une instance simple du servicemanager')
		self.assertIsInstance(ServiceManager.get_instance(), ServiceManager)
		

	def test_get_unique_instance(self):
		print('\ntest de l\'unicité du servicemanager')
		sm1 = ServiceManager.get_instance()
		sm2 = ServiceManager.get_instance()
		self.assertEqual(sm1, sm2)
		

	#test de manipulation des services
	def test_create_service(self):
		print('\ntest de l\'enregistrement d\'un service comme available')
		service_manager = ServiceManager.get_instance()
		service_interface = ServiceInterface()
		self.assertEqual(service_manager.create_service('dummy', service_interface), True)
		self.assertEqual(service_interface, service_manager._services_available['dummy'])


	def test_create_already_existing_service(self):
		print('\ntest de la creation d\'un service deja existant')
		service_manager = ServiceManager.get_instance()
		service_interface = ServiceInterface()
		self.assertEqual(service_manager.create_service('dummy', service_interface), True)
		self.assertEqual(service_manager.create_service('dummy', service_interface), False)


	def test_delete_service(self):
		print('\ntest de la destruction d\'un service comme available')
		service_manager = ServiceManager.get_instance()
		service_interface = ServiceInterface()
		self.assertEqual(service_manager.create_service('dummy', service_interface), True)
		self.assertEqual(service_manager.delete_service('dummy'), True)


	def test_enable_available_service(self):
		print('\ntest de l\'activation d\'un service')
		service_manager = ServiceManager.get_instance()
		service_interface = ServiceInterface()
		self.assertEqual(service_manager.create_service('dummy', service_interface), True)
		self.assertEqual(service_manager.enable_service('dummy'), True)
		self.assertEqual(service_interface, service_manager._services_enable['dummy'])


	def test_enable_not_available_service(self):
		print('\ntest de l\'activation d\'un service non available')
		service_manager = ServiceManager.get_instance()
		self.assertEqual(service_manager.enable_service('dummy'), False)


	def test_disable_service(self):
		print('\ntest de la desactivation d\'un service')
		service_manager = ServiceManager.get_instance()
		service_interface = ServiceInterface()
		self.assertEqual(service_manager.create_service('dummy', service_interface), True)
		self.assertEqual(service_manager.enable_service('dummy'), True)


	def test_disable_service_not_available(self):
		print('\ntest de la desactivation d\'un service')
		service_manager = ServiceManager.get_instance()
		self.assertEqual(service_manager.disable_service('dummy'), False)


	def test_disable_service_not_enabled(self):
		print('\ntest de la desactivation d\'un service qui na jamais été activé')
		service_manager = ServiceManager.get_instance()
		service_interface = ServiceInterface()
		self.assertEqual(service_manager.create_service('dummy', service_interface), True)
		self.assertEqual(service_manager.disable_service('dummy'), False)


	def test_get_service_available(self):
		print('\nTest de la recuperation  et du lancement d\'un service available')
		service_manager = ServiceManager.get_instance()
		service_interface = ServiceInterface()
		self.assertEqual(service_manager.create_service('dummy', service_interface), True)
		self.assertEqual(service_manager.get_service('dummy'), service_interface)
		self.assertEqual(service_interface, service_manager._services_enable['dummy'])


	def test_get_service_enable(self):
		print('\nTest de la recuperation  et du lancement d\'un service enable')
		service_manager = ServiceManager.get_instance()
		service_interface = ServiceInterface()
		self.assertEqual(service_manager.create_service('dummy', service_interface), True)
		self.assertEqual(service_manager.enable_service('dummy'), True)
		self.assertEqual(service_manager.get_service('dummy'), service_interface)
		self.assertEqual(service_interface, service_manager._services_enable['dummy'])


	def test_get_service_not_available(self):
		print('\nTest de la recuperation  et du lancement d\'un service inexistant')
		service_manager = ServiceManager.get_instance()
		self.assertEqual(service_manager.get_service('dummy'), None)


if __name__ == '__main__':
    unittest.main()