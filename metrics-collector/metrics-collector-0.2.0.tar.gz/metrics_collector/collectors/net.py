from base import CollectorThread
from ..utils import get_server_interfaces, is_private
import psutil

class NetworkCollector(CollectorThread):
	identifier = 'net'

	def __init__(self):
		self.interfaces = get_server_interfaces()

	def collect(self, cache):
		stats = psutil.net_io_counters(pernic=True)

		collected = []

		if 'prev' in cache:
			prev = cache['prev']

			for prev_if, data in cache['prev'].iteritems():
				if prev_if.startswith('lo'):continue
				collected.append({
					"measurement": 'system.net.pri' if is_private(self.interfaces[prev_if]) else 'system.net.pub',
					"fields": {
						"bytes_tx": (stats[prev_if].bytes_sent - prev[prev_if].bytes_sent),
						"bytes_rx": (stats[prev_if].bytes_recv - prev[prev_if].bytes_recv),
						"packets_tx": (stats[prev_if].packets_sent - prev[prev_if].packets_sent),
						"packets_rx": (stats[prev_if].packets_recv - prev[prev_if].packets_recv),
						"errors_in": (stats[prev_if].errin - prev[prev_if].errin),
						"errors_out": (stats[prev_if].errout - prev[prev_if].errout),
						"dropped_in": (stats[prev_if].dropin - prev[prev_if].dropin),
						"dropped_out": (stats[prev_if].dropout - prev[prev_if].dropout)
					}
				})

		# Update 'prev' data
		cache['prev'] = stats

		return collected
