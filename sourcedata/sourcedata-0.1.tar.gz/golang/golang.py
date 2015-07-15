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


def expr(x, int_type="int", float_type="float64", precision=12):
	if isinstance(x, str):
		return None, '`%s`' % x
	elif isinstance(x, numbers.Integral):
		return int_type, str(int(x))
	elif isinstance(x, numbers.Real):
		return float_type, str(float(x))
	elif isinstance(x, (list, tuple, np.ndarray)):
		x = np.asarray(x)
		if x.dtype.kind == "i":
			scalar_type = int_type
			fmt = "%d"
		elif x.dtype.kind == "f":
			scalar_type = float_type
			fmt = "%.{precision}f".format(precision=precision)
		else:
			raise TypeError("unknown array datatype: %s", x.dtype)

		array_type = "[]"*x.ndim + scalar_type
		return None, array_type + array(x, fmt)
	else:
		raise TypeError("%s cannot be serialized to c++ source" % type(x).__name__)


def dump(variables, f, indent=4, **kwargs):
	close = False
	if isinstance(f, str):
		f = open(f, "w")
		close = True

	for varname, value in variables.items():
		golangtype, golangval = expr(value, **kwargs)
		if golangtype is None:
			lhs = "var %s = " % varname
		else:
			lhs = "var %s %s = " % (varname, golangtype)
		indentation = "\n" + " " * len(lhs)
		rhs = indentation.join(golangval.split("\n"))
		f.write(lhs + rhs + "\n")

	if close:
		f.close()


def dumps(variables, **kwargs):
	f = io.StringIO()
	dump(variables, f, **kwargs)
	return f.getvalue()
