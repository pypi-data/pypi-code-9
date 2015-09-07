from base import CollectorThread

import psutil

class MemoryCollector(CollectorThread):
	identifier = 'memory'

	def collect(self, cache):
		mem = psutil.virtual_memory()

		return [{
			"measurement": "system.memory",
			"fields": {
				'total': mem.total,
				'available': mem.available,
				'used': mem.used,
			}
		}]
