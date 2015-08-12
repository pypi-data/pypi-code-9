#!/usr/bin/env python3

#
# Maynard
# Copyright 2013 by Larry Hastings
#
# An round-trip-able assembler / disassembler for Python 3.3
#
#
# TODO:
# * annotations?
# * nonlocals
#	* these are "cell" variables
#	* load_deref / store_deref / delete_deref
#   * other things are "cell" variables too?
# * extended_arg for jumps when calculating labels
# * recursive code object disassembly
#   (you can't round-trip anything useful until this works!)
#

import builtins
import collections
import __future__
import inspect
import io
import itertools
import marshal
import os
import string
import sys
import sysconfig
import types

# @all decorator makes a class/method public
__all__ = []
def all(symbol):
	__all__.append(symbol.__name__)
	return symbol


from .constants import *
from dis import HAVE_ARGUMENT


class NameTable:
	def __init__(self, name, namespace, *, allow_duplicates=False):
		self.name = name
		self.names = []
		self.values = []
		self.namespace = namespace
		self.allow_duplicates = allow_duplicates

	def __repr__(self):
		return '<NameTable ' + self.name + " " + ",".join(self.names) + '>'

	def __len__(self):
		return len(self.names)

	def __getitem__(self, name):
		return self.values[self.names.index(name)]

	def __setitem__(self, name, value):
		if not self.allow_duplicates:
			assert name[0].isalpha() or name[0].startswith('_'), "bad " + self.name + " " + repr(name) + " (must start with A-Z or a-z or _)"
			assert name not in self.namespace, "can't reuse name " + repr(name)
		self.names.append(name)
		self.values.append(value)

	def append(self, name, value=None):
		self[name] = value
		return self.names.index(name)

	def ensure(self, name, value=None):
		if not name:
			if value not in self.values:
				self.names.append(None)
				self.values.append(value)
			return self.values.index(value)
		if name not in self.names:
			index = len(self.names)
			self.append(name, value)
		else:
			index = self.names.index(name)
			assert self.values[index] == value, "self.names.index(" + repr(name) + ") is " + str(self.names.index(name)) + ", expected " + str(value)
		return index

	def __iter__(self):
		return iter(self.names)

	def __contains__(self, name):
		return name in self.names

	def index(self, name):
		return self.names.index(name)

	def find(self, name):
		try:
			return self.names.index(name)
		except ValueError:
			return -1

	def get(self, key, default=None):
		try:
			return self[key]
		except KeyError:
			return default


def print_decimal(bytecode):
	line = ""
	for i in bytecode:
		if line:
			line += ' '
		s = str(i)
		line += s
	print(line)

def bytecode_iterator(program, *, want_offset=False):
	i = 0
	while i < len(program):
		op = program[i]
		if op < argument_threshold:
			oparg = None
			increment = 1
		else:
			oparg = program[i + 1] + (program[i + 2] << 8)
			increment = 3
		if want_offset:
			yield i, op, oparg
		else:
			yield op, oparg
		i += increment


def idify(s):
	legal_for_id = string.ascii_letters + string.digits + "_"
	s = s.replace(' ', '_')
	s = s.replace(':', '_colon_')
	return ''.join([c for c in s if c in legal_for_id]).rstrip('_')


@all
def read_pyc(f):
	# first, just ignore the first twelve bytes.
	# (that's magic code, timestamp, and size)
	_ = f.read(12)
	code = marshal.load(f)
	return code

oparg_to_flags_map = {
	op_call_function: [('positional', 0, 8), ('p', 0, 8), ('kwonly', 8, 16), ('kw', 8, 16)],

}

def oparg_to_flags(op, oparg, *, want_zeroes=False):
	d = collections.OrderedDict()
	mask_used = 0
	for name, lower, upper in oparg_to_flags_map.get(op, ()):
		mask = ((1 << (upper - lower)) - 1) << lower
		if mask & mask_used:
			continue
		mask_used |= mask
		value = oparg & mask
		if value or want_zeroes:
			d[name] = value >> lower
	return d

def flags_to_oparg(op, **kw):
	unused = set(kw)
	used = set()
	accumulator = 0
	mask_used = 0
	for name, lower, upper in oparg_to_flags_map.get(op, ()):
		value = kw.get(name)
		if value is not None:
			bound = 1 << (upper - lower)  # 1<<x == 2**x
			if value > bound:
				sys.exit("Out of bounds value (" + repr(value) + " for " + name + " field for " + reverse_base_opcodes[op] + " instruction")
			mask = (bound - 1) << lower
			if mask_used & mask:
				sys.exit("Specified overlapping fields to " + reverse_base_opcodes[op] + "! " + repr(kw))
			mask_used |= mask
			accumulator |= value << lower
			unused.discard(name)
	if unused:
		sys.exit("Unknown parameters to " + reverse_base_opcodes[op] + " instruction: " + repr(unused))
	return accumulator


def list_to_flags_dict(list):
	d = {}
	for field in list:
		name, equals, value = field.partition('=')
		d[name] = int(value)
	return d

def text_to_flags_dict(s):
	return list_to_flags_dict(s.strip().split())


@all
def disassemble(o, *, simple=False, prefix='', f=None):
	real_print = builtins.print
	text = []
	if f == None:
		print = real_print
	elif f == str:
		def print(*a):
			text.append(' '.join(a))
	else:
		def print(*a):
			real_print(*a, file=f)

	if simple:
		sys.exit("Sorry, simple disassembly currently unsupported.")

	if not isinstance(o, (types.FunctionType, types.CodeType, io.IOBase)):
		sys.exit("Unsupported type for disassemble: " + repr(type(o)))
	if isinstance(o, types.FunctionType):
		fn = o
		code = fn.__code__
		print(prefix + "def " + fn.__name__ + ":")
	elif isinstance(o, types.CodeType):
		fn = None
		code = o
	else:
		# read in the module!  so cool!
		fn = None
		code = read_pyc(o)

	program = code.co_code
	globals = code.co_names

	# map varnames back to arguments
	args_argument = int(bool(code.co_flags & CO_VARARGS))
	kwargs_argument = int(bool(code.co_flags & CO_VARKEYWORDS))

	varnames = list(code.co_varnames)
	just_locals = code.co_nlocals - (code.co_argcount + code.co_kwonlyargcount + args_argument + kwargs_argument)

	if just_locals:
		local_names = varnames[-just_locals:]
		del varnames[-just_locals:]
	else:
		local_names = []

	if kwargs_argument:
		kwargs_argument = varnames.pop()

	if args_argument:
		args_argument = varnames.pop()

	if code.co_kwonlyargcount:
		kwonly_arg_names = varnames[-code.co_kwonlyargcount:]
		del varnames[-code.co_kwonlyargcount:]
	else:
		kwonly_arg_names = []
	arg_names = varnames

	varnames = code.co_varnames

	if not fn:
		defaults = []
		kwonly_defaults = {}
	else:
		defaults = fn.__defaults__ or []
		kwonly_defaults = fn.__kwdefaults__

	# declare arguments
	assert len(arg_names) == code.co_argcount, "len(" + repr(arg_names) + ") != code.co_argcount " + repr(code.co_argcount)
	if arg_names:
		o = object()
		args = reversed(list(itertools.zip_longest(reversed(arg_names), reversed(defaults), fillvalue=o)))
		for name, default in args:
			if default is not o:
				name += " " + repr(default)
			print(prefix + "    arg", name)
		print()

	assert len(kwonly_arg_names) == code.co_kwonlyargcount
	if kwonly_arg_names:
		for name in kwonly_arg_names:
			print(prefix + "    kwonly", name, str(kwonly_defaults.get(name, '???')))
		print()

	if args_argument:
		print(prefix + "    args", args_argument)

	if kwargs_argument:
		print(prefix + "    kwargs", kwargs_argument)

	# declare globals table
	if code.co_names:
		for name in code.co_names:
			print(prefix + "   ", "global", name)
		print()

	# declare constants table
	const_names = []
	if code.co_consts:
		for i, value in enumerate(code.co_consts):
			name = None
			if value in (None, True, False):
				name = 'const_' + repr(value)
			elif isinstance(value, str):
				name = 'const_str_' + idify(value)
			elif isinstance(value, int):
				name = 'const_int_' + str(value)
			if (not name) or (name in const_names):
				name = 'const_index' + str(i)
			const_names.append(name)
			print(prefix + "    const", name, repr(value))
		print()

	# declare locals
	if local_names:
		for name in local_names:
			print(prefix + "    local", name)
		print()

	# look for jump targets so we can print labels
	jump_targets = set()
	for offset, op, oparg in bytecode_iterator(program, want_offset=True):
		if op in all_jumps:
			assert oparg is not None
			if op in relative_jumps:
				oparg += offset + 3
			jump_targets.add(oparg)

	for offset, op, oparg in bytecode_iterator(program, want_offset=True):
		if offset in jump_targets:
			print("label_" + str(offset) + ":")
		if oparg is None:
			oparg = ''
		if op in all_jumps:
			assert oparg is not None
			if op in relative_jumps:
				oparg += offset + 3
			oparg = "label_" + str(oparg)
		elif op in all_locals:
			oparg = varnames[oparg]
		elif op in all_names:
			oparg = globals[oparg]
		elif op in all_consts:
			oparg = const_names[oparg]
		if op in oparg_to_flags_map:
			d = oparg_to_flags(op, oparg, want_zeroes=True)
			args = " ".join(name + "=" + str(value) for name, value in d.items())
		else:
			args = str(oparg)
		print("   ", reverse_base_opcodes[op], args)

	print("    end")
	print()

	if f is str:
		return "\n".join(text)


@all
class SimpleAssembler:
	"""
	Bare-metal translator from opcodes and arguments
	into bytecodes.  Doesn't support any tables
	(consts, names).
	"""

	class LnoTab:
		"""
		This assumes lineno and program in assembler are always up-to-date.
		"""

		def __init__(self, assembler):
			self.assembler = assembler
			self._lnotab = []
			self.firstlineno = self.lineno = assembler.lineno
			self.bytecode_offset = assembler.bytecode_offset

		def update(self):
			lineno = self.assembler.lineno
			bytecode_offset = self.assembler.bytecode_offset
			while True:
				bytecode_delta = bytecode_offset - self.bytecode_offset
				assert bytecode_delta >= 0

				lineno_delta = lineno - self.lineno
				assert lineno_delta >= 0

				# "there's a deep assumption that byte code offsets
				#  and their corresponding line #s
				#  both increase monotonically"
				#
				# in other words, if they didn't *both* change,
				# don't add a new lnotab entry.
				if not (bytecode_delta and lineno_delta):
					break

				# "when the addr field increments by more than 255,
				#  the line # increment in each pair generated must be 0
				# until the remaining addr increment is < 256".
				#
				# by "addr" they meant "bytecode offset".
				if bytecode_delta > 255:
					bytecode_delta = 255
					lineno_delta = 0
				elif lineno_delta > 255:
					lineno_delta = 255

				self._lnotab.append(bytecode_delta)
				self._lnotab.append(lineno_delta)
				self.bytecode_offset += bytecode_delta
				self.lineno += lineno_delta
				continue

		@property
		def lnotab(self):
			return bytes(self._lnotab)

	@property
	def bytecode_offset(self):
		return len(self.program)

	def __init__(self, lineno=1):
		self.lineno = lineno
		self.program = []
		self.opcodes = base_opcodes
		self.reverse_opcodes = reverse_base_opcodes
		self.lnotab = self.LnoTab(self)

	def set_opcode(self, offset, op, oparg=None):
		self.program[offset] = op
		if oparg is not None:
			assert op >= HAVE_ARGUMENT, "specified oparg for an op that doesn't take one (" + str(self.reverse_opcodes[op]) + ')'
			self.program[offset + 1] = oparg & 255
			self.program[offset + 2] = (oparg >> 8) & 255
		else:
			assert op < HAVE_ARGUMENT, "didn't specify an oparg for an op that requires one (" + str(self.reverse_opcodes[op]) + ')'

	def add_opcode(self, op, oparg=None):
		self.lnotab.update()
		self.program.append(op)
		if oparg is not None:
			assert op >= HAVE_ARGUMENT, "specified oparg for an op that doesn't take one (" + str(self.reverse_opcodes[op]) + ')'
			self.program.append(oparg & 255)
			self.program.append((oparg >> 8) & 255)
		else:
			assert op < HAVE_ARGUMENT, "didn't specify an oparg for an op that requires one (" + str(self.reverse_opcodes[op]) + ')'

	def assemble_line(self, line, lineno):
		self.lineno = lineno
		fields = line.split()
		token = fields[0]
		assert token in self.opcodes
		op = self.opcodes[token]

		if op < argument_threshold:
			argument = None
		else:
			assert len(fields) > 1
			argument = int(fields[1])
		self.add_opcode(op, argument)

	def assemble(self, i, lineno=None):
		if lineno is not None:
			assert lineno >= self.lineno, "you can't jump backwards in linecount!"
			self.lineno = lineno
		for lineno, line in enumerate(i, self.lineno):
			line = line.strip()
			if not line:
				continue
			if line.startswith('#'):
				continue
			stop = self.assemble_line(line, lineno)
			if stop:
				break
		self.lineno = lineno + 1

dis_sample = """
  1           0 LOAD_GLOBAL              0 (print)
              3 LOAD_FAST                0 (a)
              6 LOAD_CONST               1 ('33')
              9 BINARY_ADD
             10 CALL_FUNCTION            1 (1 positional, 0 keyword pair)
             13 POP_TOP
             14 LOAD_CONST               0 (None)
             17 RETURN_VALUE
	"""

def dis_to_local(source):
	"""
	Converts the output of the 'dis' module
	to something understood by the local assembler.
	Note that all function metadata (names, consts)
	are up to you!

	Note: this only works for very simple examples.  It
	stumbles over the '>>' annotation for jumped-to lines.
	I left it here but it's not exported; it needs lots
	of work.
	"""
	output = []
	for line in source.split('\n'):
		if len(line) < 17:
			continue
		line = line[16:].strip()
		if not line:
			continue
		fields = line.split()
		op = fields[0]
		if len(fields) > 1:
			argument = " " + fields[1]
		else:
			argument = ""
		output.append(op.lower() + argument)
	return "\n".join(output)


extended_opcodes = {}
reverse_extended_opcodes = {}
extended_opcodes_start = 10000
extended_opcode_counter = extended_opcodes_start

def _extended_opcode(name):
	global extended_opcodes
	global reverse_extended_opcodes
	global extended_opcode_counter
	assert name not in extended_opcodes
	assert extended_opcode_counter not in reverse_extended_opcodes
	op = extended_opcode_counter
	extended_opcode_counter += 1
	extended_opcodes[name] = op
	reverse_extended_opcodes[op] = name
	return op

def extended_opcode(fn):
	name = fn.__name__.lower()
	if name.startswith('op_'):
		name = name[3:]
	return _extended_opcode(name)

@extended_opcode
def op_def(): pass

@extended_opcode
def op_class(): pass

@extended_opcode
def op_arg(): pass

@extended_opcode
def op_kwonly(): pass

@extended_opcode
def op_args(): pass

@extended_opcode
def op_kwargs(): pass

@extended_opcode
def op_local(): pass

@extended_opcode
def op_global(): pass

@extended_opcode
def op_const(): pass

@extended_opcode
def op_store(): pass

@extended_opcode
def op_load(): pass

@extended_opcode
def op_end(): pass

def is_int(x):
	try:
		y = int(x)
		return True
	except ValueError:
		return False

try:
	SimpleNamespace = types.SimpleNamespace
except AttributeError:
	class SimpleNamespace:
		def __init__(self, positional, kwonly):
			self.positional = positional
			self.kwonly = kwonly


version_3_3 = (sys.version_info.major == 3) and (sys.version_info.minor == 3)
version_3_4 = (sys.version_info.major == 3) and (sys.version_info.minor == 4)
version_3_5 = (sys.version_info.major == 3) and (sys.version_info.minor == 5)

need_store_locals = version_3_3 and not (version_3_4 or version_3_5)

@all
class Assembler(SimpleAssembler):

	def __init__(self, name, type='function', lineno=1, filename='<stdin>'):
		"""
		type should be 'module', 'class', or 'function'.
		(The main difference is how locals are treated.)
		"""
		assert type in ('module', 'class', 'function')

		super().__init__(lineno=lineno)
		self.name = name
		self.type = type
		self.filename = filename

		self.namespace = ns = set()
		self.arguments = NameTable('argument', ns)
		self.kwonlys = NameTable('kwonly', ns)
		self.defaults = {}
		self.argument_with_default = None
		self.args = self.kwargs = None
		self.varnames = NameTable('varname', ns)
		# track which entries in "names" are declared slow locals (vs globals)
		# that way we can do the right thing for "load" and "store".
		self.slow_locals = set()
		self.constants = NameTable('constant', ns, allow_duplicates=True)
		self.nonlocals = NameTable('nonlocal', ns)
		self.names = NameTable('name', ns)
		self.labels = {}
		self.unseen_labels = {}
		self.opcodes = self.opcodes.copy()
		self.opcodes.update(extended_opcodes)
		self.reverse_opcodes = self.reverse_opcodes.copy()
		self.reverse_opcodes.update(reverse_extended_opcodes)
		self.max_stack_depth = 0
		self.stack_depth = 0
		self.in_declaration_block = True
		self.assembler = None
		flags = CO_OPTIMIZED
		if self.type == 'function':
			flags |= CO_NEWLOCALS
		self.flags = flags

		if self.type == 'class':
			# the user can't specify arguments for classes or modules
			# but classes in 3.3 and below take one positional argument
			# modules have zero, classes in 3.4+ have zero

			# standard stuff for classes
			add = self.add_opcode
			ensure = self.names.ensure

			if need_store_locals:
				self.arguments.append('__locals__')
				add(op_load_fast, 0)
				add(op_store_locals)
			index = self.slow_locals_ensure('__name__')
			add(op_load_name, index)
			index = self.slow_locals_ensure('__module__')
			add(op_store_name, index)
			index = self.constants.ensure(None, name)
			add(op_load_const, index)
			index = self.slow_locals_ensure('__qualname__')
			add(op_store_name, index)

	def slow_locals_ensure(self, name):
		self.slow_locals.add(name)
		return self.names.ensure(name, name)

	def make_code_object(self):
		argcount = len(self.arguments)
		kwonlyargcount = len(self.kwonlys)

		total_nlocals = len(self.varnames)
		nlocals = total_nlocals - (argcount + kwonlyargcount)
		cellvars = ()
		freevars = ()

		flags = self.flags
		if not (cellvars or freevars):
			flags |= CO_NOFREE

		if self.args:
			flags |= CO_VARARGS
		if self.kwargs:
			flags |= CO_VARKEYWORDS

		lnotab = self.lnotab.lnotab
		code_object = types.CodeType(
			argcount,                 # argcount
			kwonlyargcount,           # kwonlyargcount
			total_nlocals,            # nlocals
			self.max_stack_depth,     # stacksize
			flags,                    # flags
			bytes(self.program),      # codestring
			tuple(self.constants.values), # constants
			tuple(self.names),        # names
			tuple(self.varnames),     # varnames
			'<stdin>',                # filename
			self.name or '',          # name (of function)
			self.lnotab.firstlineno,  # firstlineno
			lnotab,                   # lnotab
			freevars,                 # freevars
			cellvars,                 # cellvars
			)

		# print("def " + self.name + ":")
		# disassemble(code_object)
		# dis.dis(code_object)
		return code_object

	def argdefs(self):
		positional = []
		for name in self.arguments:
			if name in self.defaults:
				positional.append(self.defaults[name])
			else:
				assert not positional

		kwonly = []
		for name in self.kwonlys:
			assert name in self.defaults
			kwonly.append((name, self.defaults[name]))

		return SimpleNamespace(
			positional=tuple(positional),
			kwonly=tuple(kwonly),
			)

	def make_callable(self, globalz):
		code_object = self.make_code_object()
		f = types.FunctionType(code_object, globalz, self.name, self.argdefs().positional)
		print(self.name, "ARGDEFS KWONLY", self.argdefs().kwonly)
		if self.argdefs().kwonly:
			print("ARGDEFS KWONLY", self.argdefs().kwonly)
			f.__kwdefaults__ = dict(self.argdefs().kwonly)
		return f

	def make_module(self, module=None):
		if not module:
			module = types.ModuleType(self.name)
			module.__dict__['__builtins__'] = builtins.__dict__
		callable = self.make_callable(module.__dict__)
		disassemble(callable)
		callable()
		return module

	def add_opcode(self, op, argument=None):
		super().add_opcode(op, argument)
		if op < extended_opcodes_start:
			delta = stack_effect(op, argument)
			if delta != 0:
				assert isinstance(delta, int), "delta " + repr(delta) + " is type " + repr(type(delta))
				self.stack_depth += delta
				self.max_stack_depth = max(self.stack_depth, self.max_stack_depth)

	def ensure_return_none(self):
		if (not self.program) or (self.program[-1] != op_return_value):
			# manually add a return None
			index = self.constants.ensure(None, None)
			self.add_opcode(op_load_const, index)
			self.add_opcode(op_return_value)
			self.lnotab.update()

	def assemble(self, i, lineno=None, end=True):
		super().assemble(i, lineno=lineno)
		if end:
			self.ensure_return_none()

	def assemble_line(self, line, lineno):
		self.lineno = lineno
		if self.assembler:
			if self.assembler.assemble_line(line, lineno):
				self.assembler.ensure_return_none()
				code_object = self.assembler.make_code_object()
				name = self.assembler.name
				argdefs = self.assembler.argdefs()

				assert self.assembler.type in ('function', 'class'), "unrecognized type " + repr(self.assembler.type) + " used in sub-assembler"
				if self.assembler.type == 'class':
					# LOAD_BUILD_CLASS
					self.add_opcode(op_load_build_class)

				# for def(a, b, c=100, d=150, *, e=200)
				#
				# 3.3 stack for MAKE_FUNCTION:
				#     "e"  # kwonly name
				#     200  # kwonly value
				#     100  # positional argument 1
				#     150  # positional argument 2
				#
				# they reversed it in 3.4+!
				# 3.4 stack for MAKE_FUNCTION:
				#     100  # positional argument 1
				#     150  # positional argument 2
				#     "e"  # kwonly name
				#     200  # kwonly value
				def dump_kwonlys():
					for n, value in argdefs.kwonly:
						index = self.constants.ensure(None, n)
						self.add_opcode(op_load_const, index)
						index2 = self.constants.ensure(None, value)
						self.add_opcode(op_load_const, index2)

				if version_3_3:
					dump_kwonlys()
				for value in argdefs.positional:
					index = self.constants.ensure(None, value)
					self.add_opcode(op_load_const, index)
				if not version_3_3:
					dump_kwonlys()


				# LOAD_CONST <code object>
				index = self.constants.ensure(None, code_object)
				self.add_opcode(op_load_const, index)

				# LOAD_CONST <qualname>
				index = self.constants.ensure(None, name)
				self.add_opcode(op_load_const, index)

				function_flags = len(argdefs.positional) | (len(argdefs.kwonly) << 8)

				# MAKE_FUNCTION <positional> & 0xff | (<kw> >> 8) & 0xff | (<annotations> >> 16 & 0x7fff)
				self.add_opcode(op_make_function, function_flags)

				if self.assembler.type == 'class':
					# LOAD_CONST <qualname> (again)
					self.add_opcode(op_load_const, index)

					# CALL_FUNCTION 2 <positional> & 0xff | (<kw> >> 8) & 0xff | (<annotations> >> 16 & 0x7fff)
					self.add_opcode(op_call_function, 2)

				if self.type == 'function':
					# STORE_FAST <fast local offset>
					index = self.varnames.ensure(name)
					self.add_opcode(op_store_fast, index)
				else:
					# STORE_NAME <names array offset>
					index = self.slow_locals_ensure(name)
					self.add_opcode(op_store_name, index)

				self.assembler = None
			return

		fields = line.split()
		token = fields[0]

		# handle hash in first token
		# todo: make this less special-case-y
		if '#' in token:
			token, _, _ = token.partition('#')
			fields = [token]

		op = self.opcodes.get(token, None)

		if op in (op_arg, op_kwonly):
			assert self.in_declaration_block
			assert self.type == 'function', "arg and kwonly are only permitted inside a function"
			name = fields[1]
			ns = self.arguments if op == op_arg else self.kwonlys
			ns.append(name)
			if len(fields) > 2:
				self.argument_with_default = name
				self.defaults[name] = eval(fields[2])
			else:
				assert not self.argument_with_default, "can't have an argument without a default (" + repr(name) + ") after an argument with a default (" + repr(self.argument_with_default) + ")"
			return

		if op in (op_args, op_kwargs):
			assert self.in_declaration_block
			assert self.type == 'function', "args and kwargs are only permitted inside a function"
			key = "args" if op == op_args else "kwargs"
			d = self.__dict__
			assert not d.get(key), "can't declare " + key + " twice (already has value " + repr(d[key]) + ")"
			assert len(fields) == 2, "wrong argument count for " + key
			d[key] = fields[1]
			return

		if op == op_local:
			assert self.in_declaration_block
			append = self.varnames.append if self.type == 'function' else self.slow_locals_ensure
			append(fields[1])
			return

		if op == op_global:
			assert self.in_declaration_block
			self.names.append(fields[1])
			return

		if op == op_const:
			# relaxed restriction: you can declare globals anytime.
			# assert self.in_declaration_block
			name = fields[1]
			assert name not in self.constants
			_, _, s = line.partition(name)
			s = s.strip()
			constant = eval(s)
			self.constants.append(name, constant)
			return

		if self.in_declaration_block:
			# if we reach this point, we're done declaring things--
			# arguments, locals, constants, etc.
			self.in_declaration_block = False

			# until this point we stored arguments and fast locals
			# separately--but in the final code object they're
			# really both fast locals.  so we recompute the "varnames"
			# array and put all the arguments first.
			#
			# the order is:
			#   1. positional arguments, if any
			#   2. keyword-only arguments, if any
			#   3. *args, if used
			#   4. **kwargs, if used
			#   5. fast locals, if any
			#
			# for everything except *args and **kwargs,
			# they must be inserted into the array in the
			# order they were declared.

			fast_locals = self.varnames
			self.varnames = NameTable('varname', fast_locals.namespace)
			specials = []
			if self.args:
				specials.append(self.args)
			if self.kwargs:
				specials.append(self.kwargs)
			for name in itertools.chain(self.arguments, self.kwonlys, specials, fast_locals):
				self.varnames.append(name)

		# look for labels
		if token.endswith(':'):
			token = token[:-1]
			assert token[0].isalpha(), "bad label " + repr(name) + " (must start with A-Z or a-z)"
			assert token not in self.labels
			position = self.bytecode_offset
			self.labels[token] = position
			fixups = self.unseen_labels.get(token)
			if fixups:
				for fixup in fixups:
					op = self.program[fixup]
					self.set_opcode(fixup, op, position)
				del self.unseen_labels[token]
			return

		assert op not in (None, -1), "invalid token " + repr(token)

		if op == op_def:
			name, colon, etc = fields[1].partition(':')
			assert colon, "function name requires a colon"
			assert not etc.strip(), "illegal to have any text after the colon on a def line"
			self.assembler = Assembler(name, 'function', lineno=lineno)
			return

		if op == op_class:
			name, colon, etc = fields[1].partition(':')
			assert colon, "class name requires a colon"
			assert not etc.strip(), "illegal to have any text after the colon on a class line"
			a = self.assembler = Assembler(name, 'class', lineno=lineno)
			return

		if op == op_end:
			return True

		if op in absolute_jumps:
			name = fields[1]
			if not name[0].isdigit():
				position = self.labels.get(name)
				if position is None:
					fixups = self.unseen_labels.setdefault(name, [])
					fixups.append(len(self.program))
					position = 0
				self.add_opcode(op, position)
				return

		if op in (op_load, op_store):
			name = fields[1]
			index = self.names.find(name)
			if index != -1:
				ops = ((op_load_global, op_store_global), (op_load_name, op_store_name))
				op = ops[name in self.slow_locals][op == op_store]
			else:
				index = self.varnames.find(name)
				if index != -1:
					op = op_load_fast if op == op_load else op_store_fast
				else:
					index = self.constants.find(name)
					if index != -1:
						assert not op == op_store, "you can't store to constants!  that's what makes them constant."
						op = op_load_const
					else:
						# if we don't know what it is, assume it's a global / builtin we haven't seen yet.
						raise RuntimeError("Unknown name " + repr(name) + " for " + reverse_extended_opcodes.get(op, str(op)))

		if op == op_load_global:
			name = fields[1]
			index = self.names.find(name)
			if index == -1:
				index = len(self.names)
				self.names.append(name)
			self.add_opcode(op_load_global, index)
			return

		if op == op_load_const:
			index = self.constants.find(fields[1])
			if index != -1:
				self.add_opcode(op_load_const, index)
				return

		if op in (op_load_name, op_load_fast):
			if op == op_load_name:
				assert self.type != 'function', "can't use load_name at function scope"
			else:
				assert self.type == 'function', "can't use load_fast at global (module) or class scope"
			name = fields[1]
			index = self.varnames.find(name)
			if index is not None:
				self.add_opcode(op, index)
				return

		if op == op_store_global:
			name = fields[1]
			index = self.names.find(name)
			if index == -1:
				index = len(self.names)
				self.names.append(name)
			self.add_opcode(op_store_global, index)
			return

		if op in (op_store_name, op_store_fast):
			if op == op_store_name:
				assert self.type != 'function', "can't use store_name at function scope"
			else:
				assert self.type == 'function', "can't use store_fast at global (module) or class scope"
			name = fields[1]
			locals = self.varnames if op == op_store_fast else self.names
			index = locals.find(name)
			if index is not None:
				self.add_opcode(op, index)
				return

		if op == op_delete_fast:
			name = fields[1]
			index = self.locals.find(name)
			if index is not None:
				self.add_opcode(op_delete_fast, index)
				return

		if op in oparg_to_flags_map:
			if len(fields) == 1:
				argument = 0
			elif (len(fields) == 2) and is_int(fields[1]):
				argument = int(fields[1])
			else:
				argument = flags_to_oparg(op, **list_to_flags_dict(fields[1:]))
			self.add_opcode(op, argument)
			return

		return super().assemble_line(line, lineno)
