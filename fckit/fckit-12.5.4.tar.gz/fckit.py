# copyright (c) 2014-2015 fclaerhout.fr, released under the MIT license.

"Collection of prototyping functions and classes wrapping the standard library"

import xml.etree.ElementTree as ET, multiprocessing, ConfigParser, subprocess, threading, platform,\
	tempfile, httplib, sqlite3, base64, shutil, syslog, urllib, Queue, shlex, json, time, md5, sys, os

def _color_escaped(offset, string):
	return "\033[%im%s\033[m" % (30 + offset, string)

def gray(string):
	return _color_escaped(0, string)

def red(string):
	return _color_escaped(1, string)

def green(string):
	return _color_escaped(2, string)

def yellow(string):
	return _color_escaped(3, string)

def blue(string):
	return _color_escaped(4, string)

def magenta(string):
	return _color_escaped(5, string)

def cyan(string):
	return _color_escaped(6, string)

def white(string):
	return _color_escaped(7, string)

def disable_colors():
	global _color_escaped
	_color_escaped = lambda offset, string: string

DEVNULL = open(os.devnull, "w")

TRACEFD = DEVNULL # tracing disabled by default

def trace(*objects):
	strings = map(str, filter(None, objects))
	if strings:
		if TRACEFD == syslog:
			syslog.syslog(" ".join(strings))
		else:
			TRACEFD.write(yellow("+ %s\n") % " ".join(strings))

def disable_tracing():
	global TRACEFD
	TRACEFD = DEVNULL

def enable_tracing(with_syslog = False):
	global TRACEFD
	if with_syslog:
		TRACEFD = syslog
	else:
		TRACEFD = sys.stderr

class Error(Exception):
	"allow to raise Error(foo, bar, baz) and get the formatted string 'error: foo: bar: baz'"

	def __str__(self):
		return "error: %s" % ": ".join(map(str, self.args))

def Path(path, *paths):
	return os.path.expanduser(os.path.join(path, *paths))

def marshall(obj, path, extname = None, helpers = None, overwrite = False):
	"""
	If path does not exist, write $obj
	If path exists, write $obj if overwrite is set, raise Error otherwise.
	"""
	# <builtins>
	def _dict2cfg(obj, fp):
		parser = ConfigParser.ConfigParser()
		for section in obj:
			parser.add_section(section)
			for option, value in obj[section].items():
				parser.set(section, option, value)
		parser.write(fp)
	def _obj2json(obj, fp):
		json.dump(
			obj = obj,
			fp = fp)
	def _obj2xml(obj, fp): #FIXME: work for simple cases only
		def _f(obj):
			if isinstance(obj, dict):
				return "".join("<%s>%s</%s>" % (key, _f(obj[key]), key) for key in obj)
			else:
				return "%s" % obj
		fp.write(_f(obj))
	def _obj2txt(obj, fp):
		fp.write(obj)
	# </builtins>
	path = Path(path)
	if os.path.exists(path) and not overwrite:
		raise Error(path, "file exists")
	if not extname:
		_, extname = os.path.splitext(path)
	with open(path, "w") as fp:
		func = {
			".json": _obj2json,
			".ini": _dict2cfg,
			".cfg": _dict2cfg,
			".xml": _obj2xml,
			".txt": _obj2txt,
		}
		func.update(helpers or {}) # allow overriding builtins
		if extname in func:
			func[extname](obj, fp)
		else:
			raise Error(extname, "unsupported format")

def unmarshall(path, extname = None, default = None, helpers = None):
	"""
	Return file content as a dict (xml|ini|json), list (json) or string (txt) if the file exists.
	Return $default if it does not exist.
	Raise Error otherwise.
	"""
	# <builtins>
	def _cfg2dict(path):
		parser = ConfigParser.ConfigParser()
		if not parser.read(path):
			raise Error(path, "unreadable file")
		d = {}
		for section in parser.sections():
			d[section] = {key: value for key, value in parser.items(section)}
		return d
	def _json2obj(path):
		with open(path, "r") as fp:
			try:
				return json.load(fp) # might be a dict or a list
			except ValueError as exc:
				raise Error(*exc.args)
	def _xml2dict(path): #FIXME: work for simple cases only
		def _node_to_dict(node):
			if node.text:
				return node.text
			else:
				return {child.tag: _node_to_dict(child) for child in node}
		root = ET.parse(path).getroot()
		return {root.tag: _node_to_dict(root)}
	def _txt2str(path):
		with open(path, "r") as fp:
			return fp.read()
	# </builtins>
	path = Path(path)
	if os.path.exists(path):
		if not extname:
			_, extname = os.path.splitext(path)
		func = {
			".json": _json2obj,
			".ini": _cfg2dict,
			".cfg": _cfg2dict,
			".xml": _xml2dict,
			".txt": _txt2str,
		}
		func.update(helpers or {}) # allow overriding builtins
		if extname in func:
			return func[extname](path)
		else:
			raise Error(extname, "unsupported format")
	else:
		return default

def chdir(path):
	"trace and change of current working directory"
	path = Path(path)
	trace("chdir", path)
	os.chdir(path)

def mkdir(path = None):
	"""
	Create directory (equivalent to mkdir -p) and return its absolute path.
	If path is omitted, create a temp dir -- you have to remove it.
	"""
	if path:
		trace("makedirs", path)
		os.makedirs(path)
	else:
		trace("mktmpdir")
		path = tempfile.mkdtemp()
	return os.path.abspath(path)

def remove(path, reason = None):
	path = Path(path)
	trace("removing", "'%s'" % path, "(%s)" % reason if reason else None)
	if os.path.isdir(path):
		shutil.rmtree(path)
	else:
		os.remove(path)

class SubprocessCheckWrapper(object):
	"trace and execute command or raise Error if it is not available or fails"

	def __init__(self):
		self.cache = {} # do not use this object for long-running applications due to caching

	def _call(self, output = False, *args):
		trace(*args)
		image = args[0]
		if not image in self.cache:
			which = "where" if platform.uname()[0] == "Windows" else "which"
			self.cache[image] = subprocess.call((which, image), stdout = DEVNULL, stderr = DEVNULL)
		if self.cache[image] != 0:
			raise Error("%s is unavailable, please install it" % image)
		try:
			if output:
				return subprocess.check_output(args)
			else:
				return subprocess.check_call(args)
		except subprocess.CalledProcessError as exc:
			raise Error("%s" % exc)

	def check_output(self, *args): return self._call(True, *args)

	def check_call(self, *args): return self._call(False, *args)

SCW = SubprocessCheckWrapper()

check_output = SCW.check_output

check_call = SCW.check_call

def split_hoststring(string):
	"""
	Assuming the string matches username:password@hostname:port,
	return the tuple (username, password, hostname, port)
	Only hostname is required, any other missing component is set to None.
	"""
	if "@" in self:
		userpass, hostport = super(Hoststring, self).split("@")
	else:
		userpass, hostport = (None, "%s" % self)
	if ":" in userpass:
		username, password = userpass.split(":")
	else:
		username, password = (userpass, None)
	if ":" in hostport:
		hostname, port = hostport.split(":")
	else:
		hostname, port = (hostport, None)
	return (username, password, hostname, port)

def async(callback, args = None, kwargs = None, threaded = True):
	"execute callback asynchronously, use .is_alive() and .terminate() to interact"
	if threaded:
		obj = threading.Thread(target = callback, args = args or (), kwargs = kwargs or {})
		def raise_not_implemented():
			raise NotImplementedError
		obj.terminate = raise_not_implemented
	else:
		obj = multiprocessing.Process(target = callback, args = args or (), kwargs = kwargs or {})
	obj.daemon = True
	obj.start()
	time.sleep(0.1) # let worker start
	return obj

class RExec(object):
	"""
	SSH-based remote execution helper.
	Return stdout on success, raise Error on failure.
	E.g. filenames = RExec("example.com")("ls").splitlines()
	"""

	def __init__(self, hoststring, timeout = 4):
		if not hoststring or hoststring in ("localhost", "127.0.0.1"):
			self.hoststring = None
		else:
			self.hoststring = hoststring
			self.prefix = (
				"ssh",
				"-T",
				"-o", "NumberOfPasswordPrompts=0",
				"-o", "StrictHostKeyChecking=no",
				"-o", "ConnectTimeout=%i" % timeout,
				"-S", "/tmp/%s.socket" % self.hoststring, # use control master if available
				self.hoststring,
			)
			self.controlmaster = None

	def _Popen(self, args, stdout, stderr):
		trace(*args)
		try:
			return subprocess.Popen(
				args = args,
				stdout = stdout,
				stderr = stderr)
		except OSError as exc:
			raise Error(*(args[0], "...") + exc.args)

	def _start_controlmaster(self):
		assert not self.controlmaster, "control master already started"
		def callback():
			while True:
				trace("opening connection to", self.hoststring)
				p = self._Popen(
					args = self.prefix + ("-MT",),
					stdout = DEVNULL, # we don't need the login banner
					stderr = subprocess.PIPE)
				_, err = p.communicate()
				if p.returncode == 255: # broken pipe, reconnect
					continue
				else:
					raise Error(p.returncode, err) # unexpected error, die loudly
		self.controlmaster = async(callback)
	
	def close(self):
		if self.controlmaster:
			trace("closing connection to", self.hoststring)
			subprocess.Popen(
				args = self.prefix + ("-O", "exit"),
				stdout = DEVNULL,
				stderr = DEVNULL) # ignore any error
			self.controlmaster = None

	def __call__(self, *args):
		if self.hoststring:
			if not self.controlmaster:
				self._start_controlmaster()
			args = self.prefix + ("--",) + args
		p = self._Popen(
			args = args,
			stdout = subprocess.PIPE,
			stderr = subprocess.PIPE)
		out, err = p.communicate()
		if p.returncode:
			raise Error(p.returncode, err)
		return out

def http_request(
	hostname,
	port,
	method,
	path,
	username = None,
	password = None,
	timeout = 2,
	headers = None,
	body = None):
	"do a HTTP request with the specified parameters (method, credentials, etc.)"
	headers = headers or {}
	assert username and password or (not username and not password), "missing username or password"
	if username and password:
		auth = base64.encodestring("%s:%s" % (username, password)).rstrip()
		headers.update({"Authorization": "Basic %s" % auth})
	cnx = httplib.HTTPConnection(
		host = hostname,
		port = port,
		timeout = timeout)
	trace("HTTP", method, hostname, port, path, headers, body)
	cnx.request(
		method = method,
		url = path,
		headers = headers,
		body = body or "")
	res = cnx.getresponse()
	trace("HTTP", res.status, res.reason)
	return res

def check_http_request(*args, **kwargs):
	res = http_request(*args, **kwargs)
	if 400 <= res.status < 600:
		raise Error("http error %i, %s" % (res.status, res.reason)) # TODO: add log prefix
	else:
		return res

def timeout(exc, seconds, callback, *args, **kwargs):
	"execute threaded callback and wait termination for at most $seconds, raise $exc on timeout"
	q = Queue.Queue()
	def wrapper():
		q.put(callback(*args, **kwargs))
	t = threading.Thread(target = wrapper)
	t.start()
	t.join(timeout = seconds)
	if t.is_alive():
		t._Thread__stop()
		raise exc # raise timeout exception
	elif q.empty():
		raise Error("thread raised an exception")
	else:
		return q.get()

def parse_megabyte(string):
	"convert %value%%unit%-formatted string to binary megabyte number"
	for unit, factor in (
		("kB", 0.000953674),
		("K", 0.000976563), ("KiB", 0.000976563),
		("M", 1), ("Mi", 1),
		("G", 1024), ("Gi", 1024),
		("T", 1024**2), ("Ti", 1024**2),
		("P", 1024**3), ("Pi", 1024**3),
		("E", 1024**4), ("Ei", 1024**4),
		("Z", 1024**5), ("Zi", 1024**5),
		("Y", 1024**6), ("Yi", 1024**6)):
		if string.endswith(unit):
			return int(string.replace(unit, "")) * factor
	else:
		return int(string)

def identify_platform():
	"identify host platform and set global boolean variables accordingly"
	global WINDOWS, DARWIN, LINUX, DEBIAN, CENTOS, UBUNTU, UNIX
	WINDOWS = platform.uname()[0] == "Windows"
	DARWIN = platform.uname()[0] == "Darwin"
	LINUX = platform.uname()[0] == "Linux"
	DEBIAN = LINUX and os.path.exists("/etc/debian_version")
	CENTOS = LINUX and os.path.exists("/etc/centos-release")
	UBUNTU = LINUX\
		and subprocess.call(("which", "lsb_release"), stdout = DEVNULL) == 0\
		and subprocess.check_output(("lsb_release", "-i", "-s")).strip().lower() == "ubuntu"
	UNIX = DARWIN or DEBIAN or UBUNTU or CENTOS

def repl(prompt, commands, default = None, exception_cls = Exception):
	"tiny Read/Execute/Print/Loop implementation"
	while True:
		try:
			line = raw_input(prompt() if callable(prompt) else prompt)
			args = shlex.split(line)
			if not args:
				continue # empty line
			elif args[0] in ("exit", "quit", "q", "bye"):
				return
			else:
				try:
					if args[0] in commands:
						commands[args[0]](*args[1:])
					elif default:
						default(*args)
					else:
						print red("%s: command not found" % args[0])
				except exception_cls as exc:
					print red(exc)
		except KeyboardInterrupt:
			print red("interrupted")

def _get_sql_type(obj):
	if obj is None:
		return "null"
	elif type(obj) is int:
		return "integer"
	elif type(obj) is str:
		return "text"
	elif type(obj) is long:
		return "integer"
	elif type(obj) is float:
		return "real"
	elif type(obj) is buffer:
		return "blob"
	elif type(obj) is unicode:
		return "text"
	else:
		raise Error("%s: no corresponding SQL type" % type(obj))

class Storage(object):

	def __init__(self, path = None):
		self.connection = sqlite3.connect(path or ":memory:")
		if not path:
			trace("WARNING! using transient database")

	def _execute(self, sql, parameters = None):
		trace("executing %s" % sql)
		if parameters is None:
			return self.connection.execute(sql)
		else:
			trace("     with %s" % list(parameters))
			return self.connection.execute(sql, parameters)

	def _get_table_columns(self, name):
		"return pairs of column (name, type) if the table exists"
		rows = self._execute("pragma table_info(%s)" % name)
		for _, colname, coltype, _, _, _ in rows:
			yield (colname, coltype)

	def upsert(self, name, **kwargs):
		"update schema, upsert row and return its id"
		with self.connection:
			# create table if not exists:
			self._execute("create table if not exists %s(id integer primary key)" % name)
			# create columns if not exist:
			schema = tuple(pair for pair in self._get_table_columns(name))
			for colname, colvalue in kwargs.items():
				coltype = _get_sql_type(colvalue)
				for _colname, _coltype in schema:
					if _colname == colname:
						if not _coltype == coltype:
							raise Error(colname, coltype, "column exists with a different type (%s)" % _coltype)
						else:
							break
				else:
					self._execute("alter table %s add column %s %s" % (name, colname, coltype))
			# execute upsert:
			if "id" in kwargs:
				_id = kwargs["id"]
				keys, values = zip(*[(key, value) for key, value in kwargs.items() if key != "id"])
				sql = "update %s set %s where id=?" % (
					name,
					", ".join("%s=?" % key for key in keys))
				self._execute(sql, values + (_id,))
			else:
				keys, values = zip(*[(key, value) for key, value in kwargs.items()])
				sql = "insert into %s(%s) values (%s)" % (
					name,
					", ".join(keys),
					", ".join(["?"] * len(keys)))
				_id = self._execute(sql, values).lastrowid
				trace("       id=%i" % _id)
			return _id

	def select(self, name, limit = None, where = None, orderby = None, ascendant = True, **kwargs):
		"""
		Return matching rows.
		- $orderby is a list of column names.
		- The usage of $where and $kwargs is exclusive.
		  - $kwargs is interpreted as a key=value conjunction.
		  - $where can be a simple expression string, or a list (string, values...)
		"""
		with self.connection:
			sql = "select * from %s" % name
			parameters = None
			if where:
				if isinstance(where, (list, tuple)):
					sql += " where %s" % where[0]
					parameters = where[1:]
				else:
					sql += " where %s" % where
			elif kwargs:
				keys, values = zip(*[(key, value) for key, value in kwargs.items()])
				sql += " where %s" % " and ".join("%s = ?" % key for key in keys)
				parameters = values
			if orderby:
				sql += " order by %s %s" % (",".join(orderby), "asc" if ascendant else "desc")
			if limit:
				sql += " limit %i" % limit
			try:
				rows = [row for row in self._execute(sql, parameters)]
				if rows:
					keys = [key for key, _ in self._get_table_columns(name)]
				return [dict(zip(keys, row)) for row in rows]
			except sqlite3.OperationalError as exc:
				if str(exc).startswith("no such table"):
					return []
				else:
					raise

	def delete(self, name, **kwargs):
		"delete rows and return the number of deleted rows"
		with self.connection:
			sql = "delete from %s" % name
			keys, values = zip(*[(key, value) for key, value in kwargs.items()])
			if kwargs:
				expr = " and ".join("%s = ?" % key for key in keys)
				sql += " where %s" % expr
			return self._execute(sql, values).rowcount

class BuildTarget(object):
	"manage a target incremental build from its sources"

	def __init__(self, path, callback, phony = False, sources = None, exclude = None):
		self.hmap_path = os.path.join(os.path.dirname(path), ".%s.hmap" % os.path.basename(path))
		self.callback = callback
		self.sources = sources or ()
		self.exclude = exclude or ()
		self.policy = "default"
		self.phony = phony
		self.path = path
		assert\
			self.phony or not any(src.phony for src in self.sources),\
			"non-phony target has illegal phony source"

	def exists(self):
		assert not self.phony, "illegal call on phony target"
		return os.path.exists(self.path)

	def digest(self):
		assert not self.phony, "illegal call on phony target"
		if not self.exists():
			self.build()
		def filemd5(path):
			with open(path, "r") as fp:
				return md5.new(fp.read()).hexdigest()
		if os.path.isdir(self.path):
			hmap = {}
			for root, dirnames, basenames in os.walk(self.path):
				dirnames = filter(lambda name: os.path.join(root, name) not in self.exclude, dirnames)
				for name in basenames:
					path = os.path.join(root, name)
					hmap[path] = filemd5(path)
			return md5.new("%s" % hmap).hexdigest()
		else:
			return filemd5(self.path)

	def build(self, sources = None):
		"return True if the target has been updated, False otherwise"
		sources = {
			"default": lambda sources: self.sources or sources, # prefer old, use new if none
			"discard": lambda sources: self.sources, # use old sources
			"append": lambda sources: self.sources + sources, # use all sources
			"reset": lambda sources: sources, # use new sources
		}[self.policy](sources or ())
		for src in sources:
			src.build()
		if self.phony:
			self.callback(sources)
		else:
			oldhmap = unmarshall(self.hmap_path, extname = ".json", default = {})
			newhmap = {os.path.abspath(src.path): src.digest() for src in sources}
			if self.exists() and newhmap == oldhmap:
				trace("target '%s' is up to date" % self.path)
				return False
			else:
				if not os.path.exists(os.path.dirname(self.path)):
					mkdir(os.path.dirname(self.path))
				marshall(
					obj = newhmap,
					path = self.hmap_path,
					extname = ".json",
					overwrite = True) # save new hmap
				self.callback(
					path = self.path,
					sources = sources)
				assert self.exists(), "target not built -- please report this bug"
				return True
