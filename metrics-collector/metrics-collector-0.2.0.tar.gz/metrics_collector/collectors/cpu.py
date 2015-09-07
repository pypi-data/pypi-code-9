from base import CollectorThread

import psutil

class CPUCollector(CollectorThread):
	identifier = 'cpu'

	def collect(self, cache):
		return [{
			"measurement": "system.cpu",
			"fields": {
				'usage': psutil.cpu_percent()
			}
		}]
