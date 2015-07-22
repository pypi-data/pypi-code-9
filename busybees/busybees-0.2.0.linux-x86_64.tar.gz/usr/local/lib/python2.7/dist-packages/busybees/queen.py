import locked_queue
import logging
import time
import threading

# configures debug logging?
logging.basicConfig(filename='/tmp/queen.log', level=logging.DEBUG,
    format='%(asctime)s (%(threadName)-2s) %(message)s',)


class Queen(object):

	# sets its lock, schedule, name, and default worker type
	def __init__(self, name, lock, sched, default_worker):
		self.lock = lock
		self.sched = sched
		self.name = name
		self.default_worker = default_worker

	# wait for the locked queue to be unlocked, and when it is unlocked
	# append the queue contents to a working job queue
	def main(self):
		f = int(1)
		logging.debug('Starting the queen...')
		local_lock = locked_queue.LockedQueue()
		self.lock.acquire()
		logging.debug('Acquired the lock for the first time.')
		workers=[]
		die = False
		while True:
			q = self.lock.enum()
			for i in q:
				if i == 'die':
					die = True
				else:
					# pick instruction value from tuple
					instruction = i[0]
					
					# look at worker variable, if it specifies default
					# use the default passed on queen creation, else
					# use the class passed to it
					if i[1] == 'default':
						worker_var = self.default_worker
					else:
						worker_var = i[1]

					# build and start the worker
					cw = worker_var(local_lock,instruction)
					c = threading.Thread(name="%s:worker%d"%(self.name,f),target=cw.run)
					f += 1
					c.start()
					# janky way of avoiding threads starting out of order
					time.sleep(0.1)
					workers.append(c)
			if die == True:
				logging.debug('Death command received.')
				break
			else:
				self.lock.clear()
				self.lock.cond.notify()
				logging.debug('Apiary notified. Releasing...')
				self.lock.cond.wait()
				logging.debug('Reacquired the lock.')

		# dies gracefully, joining all worker threads
		logging.debug("Waiting for remaining workers...")
		for i in workers:
			i.join()
		logging.debug("No more workers in line.")

		# clears the locked queue and then appends worker results to it
		logging.debug("Sending results back to the hive...")
		self.lock.clear()
		self.lock.append(local_lock.enum())
		self.lock.release()
		# dies
		logging.debug("Queen died (gracefully, one hopes).")

