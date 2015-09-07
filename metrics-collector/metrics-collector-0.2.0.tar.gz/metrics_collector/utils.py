from Queue import Queue
from threading import Thread
import struct
import socket
import time
import psutil

class TimeoutError(Exception):
	pass

class TimedQueue(Queue):
	def join_with_timeout(self, timeout):
		self.all_tasks_done.acquire()
		try:
			endtime = time.time() + timeout
			while self.unfinished_tasks:
				remaining = endtime - time.time()
				if remaining <= 0.0:
					raise TimeoutError
				self.all_tasks_done.wait(remaining)
		finally:
			self.all_tasks_done.release()

class Worker(Thread):
	"""Thread executing tasks from a given tasks queue"""
	def __init__(self, tasks):
		Thread.__init__(self)
		self.tasks = tasks
		self.daemon = True
		self.start()

	def run(self):
		while True:
			func, args, kwargs = self.tasks.get()
			try:
				func(*args, **kwargs)
			except Exception, e:
				print e
			finally:
				self.tasks.task_done()

class ThreadPool:
	"""Pool of threads consuming tasks from a queue"""
	def __init__(self, num_threads):
		self.tasks = TimedQueue(num_threads)
		for _ in range(num_threads): Worker(self.tasks)

	def add_task(self, func, *args, **kwargs):
		"""Add a task to the queue"""
		self.tasks.put((func, args, kwargs))

	def wait_completion(self):
		"""Wait for completion of all the tasks in the queue"""
		self.tasks.join_with_timeout(0.5)

def is_private(ip):
	try:
		f = struct.unpack('!I',socket.inet_pton(socket.AF_INET,ip))[0]
		private = (
			[ 2130706432, 4278190080 ], # 127.0.0.0,   255.0.0.0   http://tools.ietf.org/html/rfc3330
			[ 3232235520, 4294901760 ], # 192.168.0.0, 255.255.0.0 http://tools.ietf.org/html/rfc1918
			[ 2886729728, 4293918720 ], # 172.16.0.0,  255.240.0.0 http://tools.ietf.org/html/rfc1918
			[ 167772160,  4278190080 ], # 10.0.0.0,    255.0.0.0   http://tools.ietf.org/html/rfc1918
		)
		for net in private:
			if f & net[1] == net[0]:
				return True
		return False
	except:
		return True

def get_server_interfaces():
	address = psutil.net_if_addrs()
	interfaces = {}
	for k, v in address.items():
		interfaces[k] = v[0].address
	return interfaces

def get_server_public_ip():
	for k,v in get_server_interfaces().items():
		if k.startswith('lo'):continue
		if not is_private(v):
			return v
	raise Exception('cannot find server public ip')
