import multiprocessing


#class ParallelFileProcessor(object):
#
#	def __init__(
#		self,
#		target,
#		in_path,
#		out_path=None,
#		chunksize=100,
#		args=[],
#		kwargs={}
#	):
#		self.file_chunker = FileChunker(fpath, chunksize)
#		if out_path is not None:
#			self.out_file = open(out_path, 'w')
#		else:
#			self.out_file = None
#		
#
#
#class FileChunker(object):
#	def __init__(self, fpath, chunksize):
#		self.fpath = fpath
#		self.f = open(fpath)
#		self.chunksize = chunksize
#
#	def __iter__(self):
#		return self
#
#	def next(self):
#
#		# Accumulate <chunksize> lines into one chunk
#		chunk = []
#		for i in range(self.chunksize):
#
#			try:
#				chunk.append(self.f.next())
#
#			# If we reach the end of the file, return the partial chunk
#			except StopIteration:
#				if len(chunk) > 0:
#					return chunk
#
#				# But if the chunk is empty, then stop iteration
#				else:
#					raise
#
#		return chunk

