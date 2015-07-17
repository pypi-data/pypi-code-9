import subprocess, random, string, os, fcntl

class LineBuffer(object):
	"""
	Processes each line in the desired buffer

	From Juan Luis Boya: https://github.com/ntrrgc/dotfiles/blob/master/wtfd
	"""
	def __init__(self):
		self.buffer = b''

	def read_lines(self, input):
		"""
		Processes each line and appends it to the buffer
		"""
		while b'\n' in input:
			before, after = input.split(b'\n', 1)
			yield self.buffer + before
			self.buffer = b''
			input = after
		self.buffer += input

class ProcessReactor(object):
	def __init__(self, user, directory, ioloop, ip, opensockets, *args, **kwargs):
		"""
		Starts the command and sets the redirection of the desired buffers
		:param pwd: user The pwd structure with the information of the user which issued the command
		:param str directory: The directory to use as cwd
		:param list: args A list of supplementary arguments
		:param dict: kwargs A dictionary of keyword arguments

		The function redirects STDOUT and STDERR to a pipe, and then executes the command using Popen.
		The output pipe descriptor is made non-blocking and included in the instance of the IOLoop. 
		"""

		self.user = user #user which executes the command
		self.command = ' '.join(*args) # The name of the command
		self.ip = ip # The IP of the server
		self.shell =  kwargs.get("shell", False)
		self.ioloop = ioloop
		def randomString():
			"""
			Generates a random token

			:returns: A random string which acts as a token
			"""
			return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(3))

		# Generates a random token to identify the execution
		self.identifier = ''.join(random.choice(string.ascii_uppercase) for i in range(12))
		
		self.opensockets  = opensockets
		
		#The buffers are redirected
		kwargs['stdout'] = subprocess.PIPE
		kwargs['stderr'] = subprocess.PIPE
		
		def demote(uid, gid):
			"""
			The UID and GID of the child process is changed to match those of the user
			who issued the command. Otherwise the operation would be executed as root.
			"""
			os.setgid(gid)
			os.setuid(uid)

		kwargs['shell'] = False
		self.process = subprocess.Popen(preexec_fn=demote(user.pw_uid, user.pw_gid), #function executed before the call
										cwd=directory, # The current working directory is changed
										*args, **kwargs)
		
		#The fileno of the stdout buffer is used to make it non-blocking
		self.fd = self.process.stdout.fileno()
		fl = fcntl.fcntl(self.fd, fcntl.F_GETFL) #The file access mode is returned
		fcntl.fcntl(self.fd, fcntl.F_SETFL, fl | os.O_NONBLOCK) # The flags of the file are modified, appending the non-blocking flag blogin

		#The same for stderr
		self.fd_err = self.process.stderr.fileno()
		fl_err = fcntl.fcntl(self.fd_err, fcntl.F_GETFL)
		fcntl.fcntl(self.fd_err, fcntl.F_SETFL, fl | os.O_NONBLOCK)

		#Creation of the line buffer
		self.line_buffer = LineBuffer()

		#Two handlers are registered, each for one of the output buffers. can_read and can_read_stderr act as the callback for events related to both of them
		self.ioloop.add_handler(self.process.stdout, self.can_read, self.ioloop.READ)
		self.ioloop.add_handler(self.process.stderr, self.can_read_stderr, self.ioloop.READ)
	
	def kill(self):
		if self.process.returncode is None:
			self.process.kill()

	def stop(self):
		if self.process.returncode is None:
			print("Sending terminate signal")
			self.process.terminate()
			self.ioloop.call_later(60, self.kill)

	def can_read(self, fd, events):
		"""
		Processes the stdout event
		:param int fd: The file descriptor of the stdout buffer
		:param int events: The event flags (bitwise OR of the constants IOLoop.READ, IOLoop.WRITE, and IOLoop.ERROR)
		"""
		data = self.process.stdout.read(1024)
		

		if len(data) > 0:
			"""If the length of the data is larger than zero, the information is sent to all
			the listening sockets"""
			self.on_data(data, "stdout")

		else:
			print("Lost connection to subprocess")
			self.ioloop.remove_handler(self.process.stdout)
			self.stop_output("stdout")
	
	def can_read_stderr(self, fd, events):
		"""
		Processes the stderr event
		:param int fd: The file descriptor of the stderr buffer
		:param int events: The event flags (bitwise OR of the constants IOLoop.READ, IOLoop.WRITE, and IOLoop.ERROR)
		"""
		data = self.process.stderr.read(1024)

		if len(data) > 0:
			self.on_data(data, "stderr")

		else:
			print("Lost connection to subprocess")
			self.ioloop.remove_handler(self.process.stderr)
			self.stop_output("stderr")

	def on_data(self, data, stream_name):
		"""
		Decodes the data and passes it to on_line
		:param bytes data: an array of bytes with the message
		:param str stream_name: The name of the stream
		"""
		for line in self.line_buffer.read_lines(data):
			self.on_line(line.decode('utf-8'), stream_name)

	def on_line(self, line, stream_name):
		"""
		Sends the line to the open websocket
		:param str line: The message line
		:param str stream_name: The name of the stream
		"""
		for ws in self.opensockets[self.user.pw_name]:
			ws.on_line(self.user.pw_name, self.command, line, self.ip, self.identifier, False, stream_name, shell=self.shell)


	def stop_output(self, stream_name="unknown"):
		"""
		Sends a special message to close the websocket connection
		"""
		for ws in self.opensockets[self.user.pw_name]:
			ws.on_line(self.user.pw_name, self.command, None, self.ip, self.identifier, True, stream_name, shell=self.shell)

