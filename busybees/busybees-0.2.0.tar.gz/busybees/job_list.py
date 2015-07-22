
# each entry contains three pieces of information:
#	1) Job id number, which must be managed and remembered
#	   by the calling function, preferably via RNG
#	2) Command that should be run, in bash syntax
#	3) The status of the job, where: (integers deprecated, do not use)
#		0 = scheduled
#		1 = current
#		2 = completed
#		3 = cancelled

class JobList(object):

	def __init__(self):
		self.queue = []

	def add(self, idnum, command):
		entry = [idnum, command, 'scheduled']
		self.queue.append(entry)

	def list_all(self):
		return self.queue

	def cancel(self, idnum):
		index = self.find_tuple(idnum, self.queue)
		assert self.queue[index][2] == 'scheduled', "Job looks like it wasn't waiting."
		self.queue[index][2] = 'cancelled'

	def curr(self, idnum):
		index = self.find_tuple(idnum, self.queue)
		assert self.queue[index][2] == 'scheduled', "Job looks like it wasn't waiting."
		self.queue[index][2] = 'current'

	def done(self, idnum):
		index = self.find_tuple(idnum, self.queue)
		assert self.queue[index][2] == 'current', "Job looks like it wasn't running."
		self.queue[index][2] = 'completed'

	def find_tuple(self, val1, q):
		for index,i in enumerate(q):
			x, y, z = i
			if x == val1:
				return index
