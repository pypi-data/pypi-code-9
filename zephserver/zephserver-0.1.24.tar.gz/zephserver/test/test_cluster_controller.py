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

from zephserver.infra.cluster_adapter import ClusterAdapter


class TestClusterController(unittest.TestCase):
	'''
		ensemble des testes unitaires pour la classe servicemanager
	'''
	#instance du serveur
	_bootstrap = None

	_test_callback= False
	
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
		cluster_adapter = ClusterAdapter.get_instance()
		cluster_adapter._stop_service = False
		cluster_adapter._suscribers = {}


	#tests du sigleton
	def test_get_instance_simple(self):
		print('\ntest de la recuperation d\'une instance simple du servicemanager')
		self.assertIsInstance(ClusterAdapter.get_instance(), ClusterAdapter)
		

	def test_get_unique_instance(self):
		print('\ntest de l\'unicité du servicemanager')
		sm1 = ClusterAdapter.get_instance()
		sm2 = ClusterAdapter.get_instance()
		self.assertEqual(sm1, sm2)

	def test_suscribe_no_event(self):
		event = 'toto'
		def callback(self):
			self._test_callback = True
		cluster_adapter = ClusterAdapter.get_instance()
		cluster_adapter.suscribe(event, callback)
		
		self.assertEqual(cluster_adapter._suscribers.has_key(event), True)
		self.assertEqual(len(cluster_adapter._suscribers), 1)
		self.assertEqual(cluster_adapter._suscribers[event][0], callback)

	def test_suscribe_alrady_event(self):
		event = 'toto'
		def callback(self):
			self._test_callback = True
		cluster_adapter = ClusterAdapter.get_instance()
		self.assertEqual(cluster_adapter.suscribe(event, callback), True)
		self.assertEqual(cluster_adapter._suscribers.has_key(event), True)
		self.assertEqual(len(cluster_adapter._suscribers[event]), 1)
		self.assertEqual(cluster_adapter._suscribers[event][0], callback)
		self.assertEqual(cluster_adapter.suscribe(event, callback), True)
		self.assertEqual(len(cluster_adapter._suscribers[event]), 2)


if __name__ == '__main__':
    unittest.main()