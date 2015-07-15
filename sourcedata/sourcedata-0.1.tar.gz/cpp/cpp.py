import io
import sys
import numbers
import collections
import numpy as np


def array(x, fmt):
	x = np.asarray(x)
	if x.ndim == 1:
		return "{" + ", ".join(fmt % xi for xi in x) + "}"
	else:
		return "{" + ",\n ".join(array(row, fmt).replace("\n", "\n ") for row in x) + "}"


def expr(x, string_type="std::string", int_type="int", float_type="double", precision=12):
	if isinstance(x, str):
		return string_type, '"%s"' % x
	elif isinstance(x, numbers.Integral):
		return int_type, str(int(x))
	elif isinstance(x, numbers.Real):
		return float_type, str(float(x))
	elif isinstance(x, (list, tuple, np.ndarray)):
		x = np.asarray(x)
		if x.dtype.kind == "i":
			cpptype = int_type
			fmt = "%d"
		elif x.dtype.kind == "f":
			cpptype = float_type
			fmt = "%.{precision}f".format(precision=precision)
		else:
			raise TypeError("unknown array datatype: %s", x.dtype)

		# We must use explicit sizes for multidimensional arrays, so just use explicit sizes always
		return cpptype+" %s" + "".join("[%d]" % n for n in x.shape), array(x, fmt)
	else:
		raise TypeError("%s cannot be serialized to c++ source" % type(x).__name__)


def dump(dict, f, namespace=None, indent=4, **kwargs):
	close = False
	if isinstance(f, str):
		f = open(f, "w")
		close = True

	prefix = ""
	if namespace:
		namespace_parts = namespace.split("::")
		f.write(" ".join("namespace %s {" % part for part in namespace_parts) + "\n")
		prefix = " "*indent

	for varname, value in dict.items():
		cpptype, cppval = expr(value, **kwargs)
		if '%s' in cpptype:
			vardecl = cpptype % varname
		else:
			vardecl = cpptype + " " + varname
		lhs = prefix + vardecl + " = "
		indentation = "\n" + " " * len(lhs)
		rhs = indentation.join(cppval.split("\n"))
		f.write(lhs + rhs + ";\n")

	if namespace:
		f.write("}" * len(namespace_parts) + "\n")

def dumps(dict, **kwargs):
	f = io.StringIO()
	dump(dict, f, **kwargs)
	return f.getvalue()
