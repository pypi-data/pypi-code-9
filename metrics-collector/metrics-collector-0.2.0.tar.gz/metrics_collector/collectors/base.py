class CollectorThread(object):
	""" A thread that runs tasks from a queue """
	def collect(self, cache):
		raise NotImplemented()

	def collect_data(self, result, cache):
		result.data = self.collect(cache)

# We use a class to ensure the reference is updated, and can't be overwritten.
class CollectorCache(object):
	def __init__(self):
		self.data = {}

	def __getitem__(self, key):
		return self.data[key]

	def __setitem__(self, key, value):
		self.data[key] = value

	def __delitem__(self, key):
		del self.data[key]

	def __iter__(self):
		return self.data.__iter__()

	def __contains__(self, item):
		return self.data.__contains__(item)

class Result(object):
	def __init__(self):
		self.data = None
