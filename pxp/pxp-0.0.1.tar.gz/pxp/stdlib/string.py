from decimal import Decimal

from pxp.function import FunctionArg, FunctionList, InjectedFunction
from pxp.stdlib.types import number_t, string_t, boolean_t


def str_endswith(resolver, subject, value):
  sval, val = resolver.resolve_all(subject, value)
  return sval.endswith(val)


def str_find(resolver, subject, value, start, end):
  sval, val, tval, nval = resolver.resolve_all(subject, value, start, end)
  return Decimal(sval.find(val, tval, nval))


def str_len(resolver, subject):
  sval = resolver.resolve(subject)
  return Decimal(len(sval))


def str_lower(resolver, subject):
  sval = resolver.resolve(subject)
  return sval.lower()


def str_replace(resolver, subject, old, new, count):
  sval, oval, nval, cval = resolver.resolve_all(subject, old, new, count)
  return sval.replace(oval, nval, int(cval))


def str_slice(resolver, subject, start, end):
  sval, tval, nval = resolver.resolve_all(subject, start, end)
  if tval is not None:
    tval = int(tval)
  if nval is not None:
    nval = int(nval)
  return sval[tval:nval]


def str_startswith(resolver, subject, value):
  sval, val = resolver.resolve_all(subject, value)
  return sval.startswith(val)


def str_strip(resolver, subject):
  sval = resolver.resolve(subject)
  return sval.strip()


def str_upper(resolver, subject):
  sval = resolver.resolve(subject)
  return sval.upper()


string_functions = FunctionList((
  InjectedFunction("str.endswith",
                   (FunctionArg(string_t, "subject"),
                    FunctionArg(string_t, "value")),
                   boolean_t,
                   str_endswith),
  InjectedFunction("str.find",
                   (FunctionArg(string_t, "subject"),
                    FunctionArg(string_t, "value"),
                    FunctionArg(number_t, "start", None),
                    FunctionArg(number_t, "end", None)),
                   number_t,
                   str_find),
  InjectedFunction("str.len", (FunctionArg(string_t, "subject"), ), number_t, str_len),
  InjectedFunction("str.lower", (FunctionArg(string_t, "subject"), ), string_t, str_lower),
  InjectedFunction("str.replace",
                   (FunctionArg(string_t, "subject"),
                    FunctionArg(string_t, "old"),
                    FunctionArg(string_t, "new"),
                    FunctionArg(number_t, "count", Decimal(-1))),
                   string_t,
                   str_replace),
  InjectedFunction("str.slice",
                   (FunctionArg(string_t, "subject"),
                    FunctionArg(number_t, "start", None),
                    FunctionArg(number_t, "end", None)),
                   string_t,
                   str_slice),
  InjectedFunction("str.startswith",
                   (FunctionArg(string_t, "subject"),
                    FunctionArg(string_t, "value")),
                   boolean_t,
                   str_startswith),
  InjectedFunction("str.strip", (FunctionArg(string_t, "subject"), ), string_t, str_strip),
  InjectedFunction("str.upper", (FunctionArg(string_t, "subject"), ), string_t, str_upper)
))
