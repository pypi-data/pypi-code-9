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


from threading import Thread
import logging

from zephserver.task.task_interface import TaskInterface

class TaskAbstract(TaskInterface):
	
	def __init__(self):
		Thread.__init__(self)

	def run(self):
		'''
			methode principale du thread
		'''
		pass

	def interrupt(self):
		'''
			methode demandant la mise a mort de la tache
			elle doit s'executer vite
		'''
		pass
		