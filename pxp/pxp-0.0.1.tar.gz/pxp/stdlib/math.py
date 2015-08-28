import math
from decimal import Decimal

from pxp.function import FunctionArg, FunctionList, InjectedFunction
from pxp.stdlib.types import number_t, boolean_t


def math_abs(resolver, value):
  val = resolver.resolve(value)
  return val if val >= 0 else -val


def math_ceil(resolver, value):
  val = resolver.resolve(value)
  return Decimal(math.ceil(val))


def math_cos(resolver, value):
  val = resolver.resolve(value)
  return Decimal(math.cos(val))


def math_degrees(resolver, value):
  val = resolver.resolve(value)
  return Decimal(math.degrees(val))


def math_floor(resolver, value):
  val = resolver.resolve(value)
  return Decimal(math.floor(val))


def math_log(resolver, value, base):
  val = resolver.resolve(value)
  bval = resolver.resolve(base)
  return Decimal(math.log(val, bval))


def math_log10(resolver, value):
  return math_log(resolver, value, Decimal(10))


def math_log2(resolver, value):
  return math_log(resolver, value, Decimal(2))


def math_pow(resolver, value, exp):
  val = resolver.resolve(value)
  xval = resolver.resolve(exp)
  return Decimal(math.pow(val, xval))


def math_radians(resolver, value):
  val = resolver.resolve(value)
  return Decimal(math.radians(val))


def math_root(resolver, value, root):
  val = resolver.resolve(value)
  rval = resolver.resolve(root)
  return Decimal(math.pow(val, Decimal(1) / rval))


def math_round(resolver, value, ndigits):
  val = resolver.resolve(value)
  dval = resolver.resolve(ndigits)
  return Decimal(round(val, int(dval)))


def math_sin(resolver, value):
  val = resolver.resolve(value)
  return Decimal(math.sin(val))


def math_sqrt(resolver, value):
  return math_root(resolver, value, Decimal(2))


def math_tan(resolver, value):
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
