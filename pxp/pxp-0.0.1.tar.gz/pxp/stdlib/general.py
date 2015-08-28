from decimal import Decimal, InvalidOperation

from pxp.function import FunctionArg, FunctionList, InjectedFunction
from pxp.stdlib.types import number_t, string_t, boolean_t


def branch_if(resolver, predicate, if_true, if_false):
  pval = resolver.resolve(predicate)
  if predicate:
    return resolver.resolve(if_true)
  else:
    return resolver.resolve(if_false)


def is_number(resolver, value):
  try:
    Decimal(resolver.resolve(value))
    return True
  except InvalidOperation:
    return False


def to_number(resolver, value):
  return Decimal(resolver.resolve(value))


def to_string(resolver, value):
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
