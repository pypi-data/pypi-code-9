import threading

# a data structure with a queue, lock, and condition


class LockedQueue(object):

	def __init__(self):
		self.queue = []
		self.lock = threading.Lock()
		self.cond = threading.Condition(self.lock)

	# explicit lock acquisition
	def acquire(self):
		self.lock.acquire()

	# explicit lock releasing
	def release(self):
		self.lock.release()

	# acquires the lock then returns the queue
	def access(self):
		self.lock.acquire()
		return self.queue

	# returns the queue
	def enum(self):
		return self.queue

	# append to the queue, additional list filter logic
	def append(self, obj):
		if type(obj) == list:
			self.queue.extend(obj)
		else:
			self.queue.append(obj)

	# clears the queue, used for tentative jobs, etc.
	def clear(self):
		self.queue = []

