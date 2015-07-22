import threading
import logging
import operator

import locked_queue
import queen_dir

import queen
import worker

# imports for high-level scheduling
import random
import job_list



# configures debug logging?
logging.basicConfig(filename='/tmp/hive.log', level=logging.DEBUG,
    format='%(asctime)s (%(threadName)-2s) %(message)s')

class Hive(object):

	# creates the 'global' queen directory using QueenDir
	def __init__(self):
		self.queens=queen_dir.QueenDir()

	# creates a new queen object
	def create_queen(self, name, default_worker=worker.Worker):
		logging.debug("Creating a queen with name \'%s\'..." %name)
		lock = locked_queue.LockedQueue()
		sched = job_list.JobList()
		cq = queen.Queen(name, lock, sched, default_worker)
		c = threading.Thread(name="%s:queen"%name,target=cq.main)
		self.queens.add_queen(name, c, lock, sched)

	# kill gracefully, sending a special "die"-marked queue
	def kill_queen(self,name):
		# code will
		if self.queens.get_queen(name).isAlive():
			if self.queens.get_stat(name) != "ded":
				logging.debug("Waiting for the lock in order to kill %s..."%name)
				self.queens.get_lock(name).acquire()
				logging.debug("Sending death command to %s..."%name)
				self.queens.get_lock(name).append('die')
				self.queens.set_stat(name, "ded")
				self.queens.get_lock(name).cond.notify()
				self.queens.get_lock(name).release()
			else:
				logging.debug("Kill command for queen \'%s\' failed: already marked for death." %name)
		else:
			logging.debug("ERROR: I tried to kill a queen (%s) who was unstarted!"%name)

	# starts the queen using the QueenDir, but only if the queen is
	# not alive, else prints an error
	def start_queen(self, name):
		if not self.queens.get_queen(name).isAlive():
			logging.debug("Starting the queen with name \'%s\'..."%name)
			self.queens.get_queen(name).start()
		else:
			logging.debug("ERROR: I tried to start a queen (%s) who was already alive!"%name)

	# Appends some instructions to the locked queue as a tuple
	# of the instruction value(s) and the worker class to use.
	# The format of the instructions will differ depending
	# on the particular implementation of the queen.
	# All instructions provided will use the worker type specified.
	# Accepts lists gracefully as individual commands (probably).
	def instruct_queen(self, name, instructions, worker_type='default'):
		self.queens.get_lock(name).acquire()
		if type(instructions) == list:
			for i in instructions:
				self.queens.get_lock(name).append((i,worker_type))
		else:
			self.queens.get_lock(name).append((instructions,worker_type))
		self.queens.get_lock(name).cond.notify()
		self.queens.get_lock(name).release()

	# die gracefully, returns a dict of results also
	def die(self):
		logging.debug("Trying to die...")
		for queen in self.queens.enum_queens():
			self.kill_queen(queen)
		for queen in self.queens.enum_queens():
			self.queens.get_queen(queen).join()
			if not self.queens.get_queen(queen).isAlive():
				logging.debug("Joined: %s" % queen)
			else:
				assert not self.queens.get_queen(queen).isAlive(), "Joined the queen \'%s\', but the thread is still alive." % queen
		results = {}
		for queen in self.queens.enum_queens():
			results[queen] = self.get_result(queen)
		logging.debug("RIP everyone")
		return results

	# log results from a queen
	def get_result(self, name):
		self.queens.set_result(name, self.queens.get_lock(name).access())
		return self.queens.get_result(name)

	# return list of queens?
	def get_queens(self):
		return self.queens.enum_queens()



