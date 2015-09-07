from base import CollectorThread

import psutil

class DiskCollector(CollectorThread):
	identifier = 'disk'

	def collect(self, cache):
		partitions = psutil.disk_partitions()

		data = []

		total_available = 0
		total_used = 0
		total_free = 0

		for part in partitions:
			usage = psutil.disk_usage(part.mountpoint)
			total_available += usage.total
			total_used += usage.used
			total_free += usage.free

		data.append({
			"measurement": "system.disk.total",
			"fields": {
				'total_available': total_available,
				'total_used': total_used,
				'total_free': total_free,
			}
		})

		return data
