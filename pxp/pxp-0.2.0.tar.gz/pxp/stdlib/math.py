import math
from decimal import Decimal

from pxp.exception import FunctionError
from pxp.function import FunctionArg, FunctionList, InjectedFunction
from pxp.stdlib.types import number_t, boolean_t


def math_abs(resolver, value):
  """Returns the absolute value of value."""
  val = resolver.resolve(value)
  return val if val >= 0 else -val


def math_ceil(resolver, value):
  """Returns value if value is a whole number, otherwise the next largest whole number."""
  val = resolver.resolve(value)
  return Decimal(math.ceil(val))


def math_cos(resolver, value):
  """Returns the cosine of value. Value must be in radians."""
  val = resolver.resolve(value)
  return Decimal(math.cos(val))


def math_degrees(resolver, value):
  """Converts a radians value to degrees."""
  val = resolver.resolve(value)
  return Decimal(math.degrees(val))


def math_floor(resolver, value):
  """Returns value if value is a whole number, otherwise the next smallest whole number."""
  val = resolver.resolve(value)
  return Decimal(math.floor(val))


def math_log(resolver, value, base):
  """Returns the log of value. If not specified, the log is a natural log with base e."""
  bval = resolver.resolve(base)

  if bval <= Decimal(0):
    raise FunctionError("Invalid log base")

  val = resolver.resolve(value)
  return Decimal(math.log(val, bval))


def math_log10(resolver, value):
  """Returns the log base 10 of value."""
  return math_log(resolver, value, Decimal(10))


def math_log2(resolver, value):
  """Returns the log base 2 of value."""
  return math_log(resolver, value, Decimal(2))


def math_pow(resolver, value, exp):
  """Returns value raised to exp."""
  val = resolver.resolve(value)
  xval = resolver.resolve(exp)
  return Decimal(math.pow(val, xval))


def math_radians(resolver, value):
  """Converts a degrees value to radians."""
  val = resolver.resolve(value)
  return Decimal(math.radians(val))


def math_root(resolver, value, root):
  """Returns the nth root of value."""
  val = resolver.resolve(value)
  rval = resolver.resolve(root)
  return Decimal(math.pow(val, Decimal(1) / rval))


def math_round(resolver, value, ndigits):
  """Rounds value to the nearest nth digit.

  If ndigits is not specified then value is rounded to the nearest whole number.
  """
  val = resolver.resolve(value)
  dval = resolver.resolve(ndigits)
  return Decimal(round(val, int(dval)))


def math_sin(resolver, value):
  """Returns the sine of value. Value must be in radians."""
  val = resolver.resolve(value)
  return Decimal(math.sin(val))


def math_sqrt(resolver, value):
  """Returns the square root of value."""
  return math_root(resolver, value, Decimal(2))


def math_tan(resolver, value):
  """Returns the tanget of value. Value must be in radians."""
  val = resolver.resolve(value)
  return Decimal(math.tan(val))



math_functions = FunctionList((
  InjectedFunction("math.abs", (FunctionArg(number_t, "value"), ), number_t, math_abs),
  InjectedFunction("math.ceil", (FunctionArg(number_t, "value"), ), number_t, math_ceil),
  InjectedFunction("math.cos", (FunctionArg(number_t, "value"), ), number_t, math_cos),
  InjectedFunction("math.degrees", (FunctionArg(number_t, "value"), ), number_t, math_degrees),
  InjectedFunction("math.floor", (FunctionArg(number_t, "value"), ), number_t, math_floor),
  InjectedFunction("math.log", (FunctionArg(number_t, "value"), FunctionArg(number_t, "base", Decimal(math.e))), number_t, math_log),
  InjectedFunction("math.log10", (FunctionArg(number_t, "value"), ), number_t, math_log10),
  InjectedFunction("math.log2", (FunctionArg(number_t, "value"), ), number_t, math_log2),
  InjectedFunction("math.pow", (FunctionArg(number_t, "value"), FunctionArg(number_t, "exp")), number_t, math_pow),
  InjectedFunction("math.radians", (FunctionArg(number_t, "value"), ), number_t, math_radians),
  InjectedFunction("math.root", (FunctionArg(number_t, "value"), FunctionArg(number_t, "root")), number_t, math_root),
  InjectedFunction("math.round", (FunctionArg(number_t, "value"), FunctionArg(number_t, "ndigits", Decimal(0))), number_t, math_round),
  InjectedFunction("math.sin", (FunctionArg(number_t, "value"), ), number_t, math_sin),
  InjectedFunction("math.sqrt", (FunctionArg(number_t, "value"), ), number_t, math_sqrt),
  InjectedFunction("math.tan", (FunctionArg(number_t, "value"), ), number_t, math_tan)
))


math_constants = {"math.pi": Decimal(math.pi),
                  "math.e": Decimal(math.e)}
