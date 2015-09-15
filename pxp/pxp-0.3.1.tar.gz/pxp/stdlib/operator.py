from decimal import Decimal

from pxp.exception import OperatorError
from pxp.function import FunctionArg, FunctionList, InjectedFunction
from pxp.stdlib.types import number_t, string_t, boolean_t


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Number Operators
def op_number_add(resolver, left, right):
  """Returns the sum of two numbers."""
  lval = resolver.resolve(left)
  rval = resolver.resolve(right)
  return lval + rval


def op_number_subtract(resolver, left, right):
  """Returns the difference of two numbers."""
  lval = resolver.resolve(left)
  rval = resolver.resolve(right)
  return lval - rval


def op_number_multiply(resolver, left, right):
  """Returns the product of two numbers."""
  lval = resolver.resolve(left)
  rval = resolver.resolve(right)
  return lval * rval


def op_number_divide(resolver, left, right):
  """Returns the quotient of two numbers."""
  rval = resolver.resolve(right)

  if rval == Decimal(0):
    raise OperatorError("Divide by 0")

  lval = resolver.resolve(left)
  return lval / rval


def op_number_modulus(resolver, left, right):
  """Returns the remainder from left / right."""
  rval = resolver.resolve(right)

  if rval == Decimal(0):
    raise OperatorError("Divide by 0")

  lval = resolver.resolve(left)
  return lval % rval


def op_number_exponentiate(resolver, left, right):
  """Returns the value of left raised to right."""
  lval = resolver.resolve(left)
  rval = resolver.resolve(right)
  return lval ** rval


def op_number_negate(resolver, arg):
  """Returns the negation of arg."""
  aval = resolver.resolve(arg)
  return -1 * aval


def op_number_null_coalesce(resolver, left, right):
  """Returns the left if left is not null, otherwise right. Right is not resolved until it is
  determined that left is null.
  """
  lval = resolver.resolve(left, none_ok=True)
  if lval is not None:
    return lval
  else:
    rval = resolver.resolve(right, none_ok=True)
    return rval


def op_number_cmp_equal(resolver, left, right):
  """Returns True if left is equal to right."""
  lval = resolver.resolve(left)
  rval = resolver.resolve(right)
  return lval == rval


def op_number_cmp_not_equal(resolver, left, right):
  """Returns True if left is not equal to right."""
  lval = resolver.resolve(left)
  rval = resolver.resolve(right)
  return lval != rval


def op_number_cmp_greater_than_or_equal(resolver, left, right):
  """Returns True if left is greater than or equal to right."""
  lval = resolver.resolve(left)
  rval = resolver.resolve(right)
  return lval >= rval


def op_number_cmp_less_than_or_equal(resolver, left, right):
  """Returns True if left is less than or equal to right."""
  lval = resolver.resolve(left)
  rval = resolver.resolve(right)
  return lval <= rval


def op_number_cmp_greater_than(resolver, left, right):
  """Returns True if left is strictly greater than right."""
  lval = resolver.resolve(left)
  rval = resolver.resolve(right)
  return lval > rval


def op_number_cmp_less_than(resolver, left, right):
  """Returns True if left is strictly less than right."""
  lval = resolver.resolve(left)
  rval = resolver.resolve(right)
  return lval < rval


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# String operators
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def op_string_add(resolver, left, right):
  """Returns the concatenation of left and right."""
  lval = resolver.resolve(left)
  rval = resolver.resolve(right)
  return lval + rval


def op_string_null_coalesce(resolver, left, right):
  """Returns the left if left is not null, otherwise right. Right is not resolved until it is
  determined that left is null.
  """
  lval = resolver.resolve(left, none_ok=True)
  if lval is not None:
    return lval
  else:
    rval = resolver.resolve(right, none_ok=True)
    return rval


def op_string_cmp_equal(resolver, left, right):
  """Returns True if left is lexicographically equal to right."""
  lval = resolver.resolve(left)
  rval = resolver.resolve(right)
  return lval == rval


def op_string_cmp_not_equal(resolver, left, right):
  """Returns True if left is not lexicographically equal to right."""
  lval = resolver.resolve(left)
  rval = resolver.resolve(right)
  return lval != rval


def op_string_cmp_greater_than_or_equal(resolver, left, right):
  """Returns True if left is lexicographically greater than or equal to right."""
  lval = resolver.resolve(left)
  rval = resolver.resolve(right)
  return lval >= rval


def op_string_cmp_less_than_or_equal(resolver, left, right):
  """Returns True if left is lexicographically less than or equal to right."""
  lval = resolver.resolve(left)
  rval = resolver.resolve(right)
  return lval <= rval


def op_string_cmp_greater_than(resolver, left, right):
  """Returns True if left is lexicographically strictly greater than right."""
  lval = resolver.resolve(left)
  rval = resolver.resolve(right)
  return lval > rval


def op_string_cmp_less_than(resolver, left, right):
  """Returns True if left is lexicographically strictly less than right."""
  lval = resolver.resolve(left)
  rval = resolver.resolve(right)
  return lval < rval


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Boolean Operators
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def op_boolean_null_coalesce(resolver, left, right):
  """Returns the left if left is not null, otherwise right. Right is not resolved until it is
  determined that left is null.
  """
  lval = resolver.resolve(left, none_ok=True)
  if lval is not None:
    return lval
  else:
    rval = resolver.resolve(right, none_ok=True)
    return rval


def op_boolean_cmp_equal(resolver, left, right):
  """Returns True if left is equal to right."""
  lval = resolver.resolve(left)
  rval = resolver.resolve(right)
  return lval == rval


def op_boolean_cmp_not_equal(resolver, left, right):
  """Returns True if left is not equal to right."""
  lval = resolver.resolve(left)
  rval = resolver.resolve(right)
  return lval != rval


def op_boolean_logical_not(resolver, arg):
  """Returns the negation of arg. If arg is True, False is returned. If arg is False, True is
  returned.
  """
  aval = resolver.resolve(arg)
  return not aval


def op_boolean_logical_and(resolver, left, right):
  """Returns True if both left and right evaluate to True, False otherwise.

  If left is not True, the value of right doesn't matter, so right will not be evaluated.
  """
  # Short circuit
  lval = resolver.resolve(left)
  if not lval:
    return False

  rval = resolver.resolve(right)
  if rval:
    return True

  return False


def op_boolean_logical_or(resolver, left, right):
  """Returns True if left or right evaluate to True, False otherwise.

  If left is True, the value of right doesn't matter, so right will not be evaluated.
  """
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
  InjectedFunction("operatorunary-", (FunctionArg(number_t, "arg"), ), number_t, op_number_negate),
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
  InjectedFunction("operatorunary!", (FunctionArg(boolean_t, "arg"), ), boolean_t, op_boolean_logical_not),
  InjectedFunction("operator&", (FunctionArg(boolean_t, "left"), FunctionArg(boolean_t, "right")), boolean_t, op_boolean_logical_and),
  InjectedFunction("operator|", (FunctionArg(boolean_t, "left"), FunctionArg(boolean_t, "right")), boolean_t, op_boolean_logical_or)
))
