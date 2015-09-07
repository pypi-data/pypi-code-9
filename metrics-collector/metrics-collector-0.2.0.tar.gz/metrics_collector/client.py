from config import DaemonConfig as Config
from manager import WorkerManager, ThreadPool
from common.logger import log
# Load default and custom collectors
import collectors

import sys, time
import importlib, inspect
import socket
from influxdb import InfluxDBClient

class Worker(object):
	""" Handles all collectors and sending of data """

	def __init__(self, config):
		""" Creates a new daemon """
		self.config = config

		# Initialize important things
		self.client = InfluxDBClient(config.influxdb['host'],
			config.influxdb['port'],
			config.influxdb['user'],
			config.influxdb['pass'],
			config.influxdb['database']
		)

		self.manager = WorkerManager(config)

		# Print the current configuration info (and hide the password)
		log.info("Endpoint set at http://%s@***:%s:%s/db/%s}",
			config.influxdb['user'],
			config.influxdb['host'],
			config.influxdb['port'],
			config.influxdb['database']
		)

		# Print out an override notice if we're setting the hostname
		if config.metrics_collector['hostname'] != socket.gethostname():
			log.info('Hostname has been overridden to be \'%s\'', config.metrics_collector['hostname'])

		self.send_pool = ThreadPool(2)

		self.register_collectors()

	def register_collectors(self):
		registered_modules = []

		# Register built-in collectors
		for name in self.config.metrics_collector['collectors']:
			try:
				importlib.import_module('.collectors.' + name, 'metrics_collector')

				registered_modules.append('metrics_collector.collectors.' + name)
			except ImportError:
				log.warn("[!] Failed to load internal collector module '%s'", name)

				continue

		for mod in registered_modules:
			for class_name, obj in inspect.getmembers(sys.modules[mod], inspect.isclass):
				if class_name is not 'CollectorThread':
					if obj.identifier:
						class_name = obj.identifier

					log.info('[+] Registering collector \'%s\'', class_name)
					self.manager.add(class_name, obj().collect_data)

	def collect(self):
		self.manager.init_pools()
		log.debug("Starting collector")

		while True:
			try:
				start_time = time.time()
				data = self.manager.collect_all()

				# Handle sending in its own thread.
				self.send_pool.add_task(self.send_metrics, data)
			except:
				log.exception('error_collecting')
			finally:
				# Wait before collecting again
				sleep_time = max(0, 1 - (time.time() - start_time))
				time.sleep(sleep_time)

	def send_metrics(self, data):
		try:
			self.client.write_points(data, time_precision='s')
		except:
			log.exception('error_send_data')
