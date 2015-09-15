"""This module contains general pxp standard library functions."""

from decimal import Decimal, InvalidOperation

from pxp.exception import FunctionError
from pxp.function import FunctionArg, FunctionList, InjectedFunction
from pxp.stdlib.types import number_t, string_t, boolean_t


def branch_if(resolver, predicate, if_true, if_false):
  """Returns if_true if predicate evaluates to true, if_false otherwise.

  predicate is resolved and evaluated first, and then only the argument that will be returned is
  resolved and evaluated.
  """
  pval = resolver.resolve(predicate)
  if predicate:
    return resolver.resolve(if_true)
  else:
    return resolver.resolve(if_false)


def is_number(resolver, value):
  """Returns True if the string value can be parsed as a number."""
  try:
    Decimal(resolver.resolve(value))
    return True
  except InvalidOperation:
    return False


def to_number(resolver, value):
  """Returns the number representation of the string value.

  This is an unchecked conversion, so if the string is not a valid number an exception will be
  thrown.
  """
  try:
    return Decimal(resolver.resolve(value))
  except InvalidOperation:
    raise FunctionError("Unable to parse string as a Number")


def to_string(resolver, value):
  """Returns the string representation of the value."""
  return str(resolver.resolve(value))


def str_to_bool(resolver, value):
  """Converts a String to a Boolean.

  The lower-case version of the value must be 'true' or 'false', otherwise an error will be thrown.
  """
  val = str(resolver.resolve(value)).lower()
  if value == "true":
    return True
  elif value == "false":
    return False
  else:
    raise FunctionError("Unable to parse string as a Boolean")


def num_to_bool(resolver, value):
  """Converts a Number to a Boolean.

  Returns False for 0 and True for all other values.
  """
  if value == Decimal(0):
    return False
  else:
    return True


def is_null(resolver, value):
  """Returns True if the value is None."""
  return resolver.resolve(value, none_ok=True) is None


general_functions = FunctionList((
  InjectedFunction("if",
                   (FunctionArg(boolean_t, "predicate"),
                    FunctionArg(number_t, "if_true"),
                    FunctionArg(number_t, "if_false")),
                   number_t,
                   branch_if),
  InjectedFunction("if",
                   (FunctionArg(boolean_t, "predicate"),
                    FunctionArg(string_t, "if_true"),
                    FunctionArg(string_t, "if_false")),
                   string_t,
                   branch_if),
  InjectedFunction("if",
                   (FunctionArg(boolean_t, "predicate"),
                    FunctionArg(boolean_t, "if_true"),
                    FunctionArg(boolean_t, "if_false")),
                   boolean_t,
                   branch_if),
  InjectedFunction("is_num", (FunctionArg(string_t, "value"), ), boolean_t, is_number),
  InjectedFunction("to_num", (FunctionArg(string_t, "value"), ), number_t, to_number),
  InjectedFunction("to_str", (FunctionArg(number_t, "value"), ), string_t, to_string),
  InjectedFunction("to_str", (FunctionArg(string_t, "value"), ), string_t, to_string),
  InjectedFunction("to_str", (FunctionArg(boolean_t, "value"), ), string_t, to_string),
  InjectedFunction("to_bool", (FunctionArg(string_t, "value"), ), boolean_t, str_to_bool),
  InjectedFunction("to_bool", (FunctionArg(number_t, "value"), ), boolean_t, num_to_bool),
  InjectedFunction("is_null", (FunctionArg(number_t, "value"), ), boolean_t, is_null),
  InjectedFunction("is_null", (FunctionArg(string_t, "value"), ), boolean_t, is_null),
  InjectedFunction("is_null", (FunctionArg(boolean_t, "value"), ), boolean_t, is_null)
))
