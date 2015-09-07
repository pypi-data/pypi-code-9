from collectors import CollectorCache, Result
from common.logger import log
from utils import ThreadPool, TimeoutError, get_server_public_ip
import time

class WorkerManager(object):
	""" Manages all of the available daemon workers """

	def __init__(self, config):
		self.workers = {}
		self.config = config
		self.server_ip = get_server_public_ip()

	def init_pools(self):
		self.pool = ThreadPool(5)

	def add(self, ident, func):
		# If it's not already assigned, assign it.
		if ident not in self.workers:
			self.workers[ident] = {
				'method': func,
				'cache': CollectorCache(),
				'result': Result()
			}

	def get(self, ident):
		if ident not in self.workers:
			raise AttributeError("Thread with identifier '%s' not found", ident)

		return self.workers[ident]

	def collect_all(self):
		data = []

		# collect results
		for ident, worker in self.workers.iteritems():
			worker['result'].data = None
			self.pool.add_task(worker['method'], worker['result'], worker['cache'])

		try:
			self.pool.wait_completion()
		except TimeoutError:
			log.warning('Timeout')

		for ident, worker in self.workers.iteritems():
			collected = worker['result'].data
			if collected:
				for point in collected:
					point.setdefault('tags', {})['ip'] = self.server_ip
					if self.config.metrics_collector['hostname']:
						point['tags']['hostname'] = self.config.metrics_collector['hostname']

					# Add extra info
					point['time'] = int(time.time())

				# Merge the lists
				data += collected

		return data

	def status(self):
		return self.workers
