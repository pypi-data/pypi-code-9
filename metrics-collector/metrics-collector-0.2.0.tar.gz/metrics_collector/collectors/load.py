from base import CollectorThread

import os
import psutil

class LoadCollector(CollectorThread):
	identifier = 'load'

	def __init__(self):
		self.processors = psutil.cpu_count()

	def collect(self, cache):
		try:
			load = os.getloadavg()
		except:
			return []

		return [{
			"measurement":"system.load",
			"fields": {
				'm1': round(load[0]/self.processors, 3),
				'm5': round(load[1]/self.processors, 3),
				'm15': round(load[2]/self.processors, 3),
			}
		}]
