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


from threading import Thread, Event, Lock
import logging, importlib, traceback

from zephserver.service.service_interface import ServiceInterface
from zephserversettings import TASKS_PATH

class RouteurService(ServiceInterface):
	'''
		Service gerant le lancement et l'execution de tache. 
		Il gere aussi le cycle de vie des tache a travers la classe 
		TaskContainer plus bas dans le fichier.
		La seule methode devant être apelle par un autre service ou une tache
		est la methode "route".
		Les autres methodes publiques sont reservé a l'usage du service manager
		et du task container
	'''
	
	_shutdown_event = Event()
	_manipulating_task_lock = Lock()
	_task_list = []

	_pending_delete_all = False
	_pending_stop = False

	def __init__(self):
		logging.info('instanciating routeur service')

	def main(self):
		logging.info('launching routeur service')
		self._shutdown_event.wait()
		self._shutdown_event.clear()

	def disable(self):
		'''
			methode d'extinction du service
		'''
		logging.warning('asking to stop routeur service')
		self._pending_stop = True
		self._stop_all_task()
		self._shutdown_event.set()
		logging.info('routeur service stoped')

	
	def enrole_task(self, task_container):
		'''
			inscrit une tache comme en cours d'execution
		'''
		try:
			self._manipulating_task_lock.acquire()
			self._task_list.append(task_container)
		except:
			return False
		finally:
			self._manipulating_task_lock.release()
		return True


	def remove_task(self, task):
		'''
			desinscrit une tache comme en cour d'execution
		'''
		try:
			self._manipulating_task_lock.acquire()
			index = self._task_list.index(task)
			del self._task_list[index]
		except:
			return False	
		finally:
			self._manipulating_task_lock.release()
		return True


	def _stop_all_task(self):
		'''
			interompt toutes les taches
		'''
		logging.info('starting to stop all tasks')
		self._pending_delete_all = True
		while len(self._task_list) > 0:
			try:
				try:
					self._manipulating_task_lock.acquire()
					task = self._task_list.pop()			
				except:
					return False
				finally:
					self._manipulating_task_lock.release()

				task.interrupt()
				task.join()
			except:
				pass

		self._pending_delete_all = False


	def route(self, request):
		'''
			principale methode d'api permetant a n'importe qui 
			de demander le lancement d'une tache en lui 
			fournissant un dictionnaire request standardise
			la methode retourne True si tout s'est bien passe et False sinon
		'''
		try:
			if request != None and self._pending_delete_all == False and self._pending_stop == False:
				task_container = TaskContainer(self, request)
				task_container.start()
				return True
			else:
				return False
		except:
			return False



class TaskContainer(Thread):
	"""classe privée servant a encapsuller les tache et a gerer leur cycle de vie"""

	#instance du taskmanager passe au constructeur pour eviter de repasser par le service manager a chaque fois
	_task_manager = None
	#la version originale de la requete donne au routeur par le i/o service
	_request = None
	#le nom de la tache (au cas ou)
	_taskname = None
	#l'identifiant de la tache en cours
	_task = None

	def __init__(self, task_manager, request):
		Thread.__init__(self)
		self._task_manager = task_manager
		self._request = request
		logging.debug('TaskContainer %s'% request)
		
	def run(self):
		#on inscrit la tache comme active
		self._task_manager.enrole_task(self)
		self._request['authorized'] = True
		task_path = self._get_task_path()
		#si le chemin ets non trouve on desinscrit la tache et on quite
		if task_path is None:
			self._task_manager.remove_task(self)
			return
		splited_path = task_path.split('/')
		#si le chemin n'est aps consitue de deux strings separe par un symbole / on quite
		if len(splited_path) != 2 :
			logging.warning('error %s is not a valide path', task_path)
			self.task_manager.remove_task(self)
			return
		#on lance la tache dans un try except au cas ou (par exemple si le chemin est vers une classe qui n'existe pas ou si la tache crash)
		try:
			#on importe le module contenant la tache
			module = importlib.import_module(splited_path[0])
			#on instancie la tache en appellant son constructeur avec en argument la requete
			self._task = getattr(module, splited_path[1])(self._request)
			#on l'execute
			if self._request['authorized']:
				self._task.main()
		except Exception, e:
			logging.warning('request : %s', self._request)
			logging.warning('task exception %s', e)
			logging.warning(traceback.format_exc())
		finally:
			#de toute façon on deinscrit la tache avant de quiter
			self._task_manager.remove_task(self)

			
			
	def _get_task_path(self):
		'''
			methode retournant le chemin vers la tache depuis le fichier routeur.py si il le trouve et None sinon
		'''
		if TASKS_PATH.has_key(self._request['task']):
			logging.debug('task %s found as %s', self._request['task'], TASKS_PATH[self._request['task']])
			return TASKS_PATH[self._request['task']]
		else:
			logging.warning('task %s not found!', self._request['task'])
			return None


	def interrupt(self):
		'''methodepropageant la demande d'interruption a la tache execute'''
		self._task.interrupt()
