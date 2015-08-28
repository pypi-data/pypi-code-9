from decimal import Decimal

from pxp.exception import OperatorError
from pxp.function import FunctionArg, FunctionList, InjectedFunction
from pxp.stdlib.types import number_t, string_t, boolean_t


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Number Operators
def op_number_add(resolver, left, right):
  lval = resolver.resolve(left)
  rval = resolver.resolve(right)
  return lval + rval


def op_number_subtract(resolver, left, right):
  lval = resolver.resolve(left)
  rval = resolver.resolve(right)
  return lval - rval


def op_number_multiply(resolver, left, right):
  lval = resolver.resolve(left)
  rval = resolver.resolve(right)
  return lval * rval


def op_number_divide(resolver, left, right):
  rval = resolver.resolve(right)

  if rval == Decimal(0):
    raise OperatorError("Divide by 0")

  lval = resolver.resolve(left)
  return lval / rval


def op_number_modulus(resolver, left, right):
  lval = resolver.resolve(left)
  rval = resolver.resolve(right)
  return lval % rval


def op_number_exponentiate(resolver, left, right):
  lval = resolver.resolve(left)
  rval = resolver.resolve(right)
  return lval ** rval


def op_number_null_coalesce(resolver, left, right):
  lval = resolver.resolve(left)
  if left is not None:
    return lval
  else:
    rval = resolver.resolve(right)
    return rval


def op_number_cmp_equal(resolver, left, right):
  lval = resolver.resolve(left)
  rval = resolver.resolve(right)
  return lval == rval


def op_number_cmp_not_equal(resolver, left, right):
  lval = resolver.resolve(left)
  rval = resolver.resolve(right)
  return lval != rval


def op_number_cmp_greater_than_or_equal(resolver, left, right):
  lval = resolver.resolve(left)
  rval = resolver.resolve(right)
  return lval >= rval


def op_number_cmp_less_than_or_equal(resolver, left, right):
  lval = resolver.resolve(left)
  rval = resolver.resolve(right)
  return lval <= rval


def op_number_cmp_greater_than(resolver, left, right):
  lval = resolver.resolve(left)
  rval = resolver.resolve(right)
  return lval > rval


def op_number_cmp_less_than(resolver, left, right):
  lval = resolver.resolve(left)
  rval = resolver.resolve(right)
  return lval < rval


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# String operators
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def op_string_add(resolver, left, right):
  lval = resolver.resolve(left)
  rval = resolver.resolve(right)
  return lval + rval


def op_string_null_coalesce(resolver, left, right):
  lval = resolver.resolve(left)
  if left is not None:
    return lval
  else:
    rval = resolver.resolve(right)
    return rval


def op_string_cmp_equal(resolver, left, right):
  lval = resolver.resolve(left)
  rval = resolver.resolve(right)
  return lval == rval


def op_string_cmp_not_equal(resolver, left, right):
  lval = resolver.resolve(left)
  rval = resolver.resolve(right)
  return lval != rval


def op_string_cmp_greater_than_or_equal(resolver, left, right):
  lval = resolver.resolve(left)
  rval = resolver.resolve(right)
  return lval >= rval


def op_string_cmp_less_than_or_equal(resolver, left, right):
  lval = resolver.resolve(left)
  rval = resolver.resolve(right)
  return lval <= rval


def op_string_cmp_greater_than(resolver, left, right):
  lval = resolver.resolve(left)
  rval = resolver.resolve(right)
  return lval > rval


def op_string_cmp_less_than(resolver, left, right):
  lval = resolver.resolve(left)
  rval = resolver.resolve(right)
  return lval < rval


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Boolean Operators
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def op_boolean_null_coalesce(resolver, left, right):
  lval = resolver.resolve(left)
  if left is not None:
    return lval
  else:
    rval = resolver.resolve(right)
    return rval


def op_boolean_cmp_equal(resolver, left, right):
  lval = resolver.resolve(left)
  rval = resolver.resolve(right)
  return lval == rval


def op_boolean_cmp_not_equal(resolver, left, right):
  lval = resolver.resolve(left)
  rval = resolver.resolve(right)
  return lval != rval


def op_boolean_logical_not(resolver, arg):
  aval = resolver.resolve(arg)
  return not aval


def op_boolean_logical_and(resolver, left, right):
  # Short circuit
  lval = resolver.resolve(left)
  if not lval:
    return False

  rval = resolver.resolve(right)
  if rval:
    return True

  return False


def op_boolean_logical_or(resolver, left, right):
  # Short circuit
  lval = resolver.resolve(left)
  if lval:
    return True

  rval = resolver.resolve(right)
  if rval:
    return True

  return False


operator_functions = FunctionList((
  InjectedFunction("operator+", (FunctionArg(number_t, "left"), FunctionArg(number_t, "right")), number_t, op_number_add),
  InjectedFunction("operator-", (FunctionArg(number_t, "left"), FunctionArg(number_t, "right")), number_t, op_number_subtract),
  InjectedFunction("operator*", (FunctionArg(number_t, "left"), FunctionArg(number_t, "right")), number_t, op_number_multiply),
  InjectedFunction("operator/", (FunctionArg(number_t, "left"), FunctionArg(number_t, "right")), number_t, op_number_divide),
  InjectedFunction("operator%", (FunctionArg(number_t, "left"), FunctionArg(number_t, "right")), number_t, op_number_modulus),
  InjectedFunction("operator^", (FunctionArg(number_t, "left"), FunctionArg(number_t, "right")), number_t, op_number_exponentiate),
  InjectedFunction("operator?", (FunctionArg(number_t, "left"), FunctionArg(number_t, "right")), number_t, op_number_null_coalesce),
  InjectedFunction("operator=", (FunctionArg(number_t, "left"), FunctionArg(number_t, "right")), boolean_t, op_number_cmp_equal),
  InjectedFunction("operator!=", (FunctionArg(number_t, "left"), FunctionArg(number_t, "right")), boolean_t, op_number_cmp_not_equal),
  InjectedFunction("operator>=", (FunctionArg(number_t, "left"), FunctionArg(number_t, "right")), boolean_t, op_number_cmp_greater_than_or_equal),
  InjectedFunction("operator<=", (FunctionArg(number_t, "left"), FunctionArg(number_t, "right")), boolean_t, op_number_cmp_less_than_or_equal),
  InjectedFunction("operator>", (FunctionArg(number_t, "left"), FunctionArg(number_t, "right")), boolean_t, op_number_cmp_greater_than),
  InjectedFunction("operator<", (FunctionArg(number_t, "left"), FunctionArg(number_t, "right")), boolean_t, op_number_cmp_less_than),

  InjectedFunction("operator+", (FunctionArg(string_t, "left"), FunctionArg(string_t, "right")), string_t, op_string_add),
  InjectedFunction("operator?", (FunctionArg(string_t, "left"), FunctionArg(string_t, "right")), string_t, op_string_null_coalesce),
  InjectedFunction("operator=", (FunctionArg(string_t, "left"), FunctionArg(string_t, "right")), boolean_t, op_string_cmp_equal),
  InjectedFunction("operator!=", (FunctionArg(string_t, "left"), FunctionArg(string_t, "right")), boolean_t, op_string_cmp_not_equal),
  InjectedFunction("operator>=", (FunctionArg(string_t, "left"), FunctionArg(string_t, "right")), boolean_t, op_string_cmp_greater_than_or_equal),
  InjectedFunction("operator<=", (FunctionArg(string_t, "left"), FunctionArg(string_t, "right")), boolean_t, op_string_cmp_less_than_or_equal),
  InjectedFunction("operator>", (FunctionArg(string_t, "left"), FunctionArg(string_t, "right")), boolean_t, op_string_cmp_greater_than),
  InjectedFunction("operator<", (FunctionArg(string_t, "left"), FunctionArg(string_t, "right")), boolean_t, op_string_cmp_less_than),

  InjectedFunction("operator?", (FunctionArg(boolean_t, "left"), FunctionArg(boolean_t, "right")), boolean_t, op_boolean_null_coalesce),
  InjectedFunction("operator=", (FunctionArg(boolean_t, "left"), FunctionArg(boolean_t, "right")), boolean_t, op_boolean_cmp_equal),
  InjectedFunction("operator!=", (FunctionArg(boolean_t, "left"), FunctionArg(boolean_t, "right")), boolean_t, op_boolean_cmp_not_equal),
  InjectedFunction("operator!", (FunctionArg(boolean_t, "arg"), ), boolean_t, op_boolean_logical_not),
  InjectedFunction("operator&", (FunctionArg(boolean_t, "left"), FunctionArg(boolean_t, "right")), boolean_t, op_boolean_logical_and),
  InjectedFunction("operator|", (FunctionArg(boolean_t, "left"), FunctionArg(boolean_t, "right")), boolean_t, op_boolean_logical_or)
))
