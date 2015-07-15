import sys
import collections

from . import cpp
from . import golang


_generators = []


def register(f, **kwargs):
	_generators.append((f, kwargs))


def generator(**kwargs):
	def inner(f):
		register(f, **kwargs)
		return f
	return inner


def main(language, package="main", stream=sys.stdout):
	if isinstance(language, str):
		if language == "cpp":
			language = cpp
		elif language == "golang":
			language = golang
		else:
			raise Exception("Unknown language: %s" % language)

	if language == golang:
		stream.write("package %s\n\n" % package)

	for generator, kwargs in _generators:
		variables = collections.OrderedDict(list(generator()))
		stream.write("// %s\n" % generator.__name__)
		language.dump(variables, stream, **kwargs)
		stream.write("\n")
