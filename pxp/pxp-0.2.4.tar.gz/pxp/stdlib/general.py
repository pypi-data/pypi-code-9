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
    raise FunctionError("Unable to parse string as a number")


def to_string(resolver, value):
  """Returns the string representation of the value."""
  return str(resolver.resolve(value))



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
  InjectedFunction("to_str", (FunctionArg(boolean_t, "value"), ), string_t, to_string)
))
