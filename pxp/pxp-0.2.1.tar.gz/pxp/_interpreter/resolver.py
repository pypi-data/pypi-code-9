"""This module contains the Resolver class which is used by pxp functions to resolve their
arguments.
"""

from decimal import Decimal

from pxp.exception import FunctionError, RuntimeError, ScopeError


class Resolver(object):
  """The Resolver class is used by pxp functions to resolve their arguments. Arguments may be
  values, variables or expressions. The resolver class handles each and returns the actual value
  represented by the argument."""

  def __init__(self, scope):
    """Initialize the Resolver instance.

    scope is a ScopeBase instance that the resolver can use to look up variables and functions.
    """
    self.scope = scope

  def resolve(self, arg, *, none_ok=False):
    """Resolve an argument.

    If arg is a tuple, it is expected to be a raw compiled argument. The first value in the tuple
    is a string representing the type, one of: {fn, var, val} and the remaining items are the
    details of that value. If arg is not a tuple it is a real value that is passed directly back
    to the caller.
    """
    if isinstance(arg, tuple):
      arg_type = arg[0]
      # NOTE: These are 'magical' string values and aren't strongly tied with the AST module.
      if arg_type == "fn":
        val = self._resolve_function(arg)
      elif arg_type == "var":
        val = self._resolve_variable(arg, none_ok=none_ok)
      elif arg_type == "val":
        val = self._resolve_value(arg)
      elif arg_type == "branch":
        val = self._resolve_branch(arg)
      elif arg_type == "switch":
        val = self._resolve_switch(arg)
      else:
        raise Exception("Unknown arg type: {0}".format(arg_type))
    else:
      val = arg

    if val is None and not none_ok:
      raise FunctionError("Unexpected null value")

    return val

  def resolve_all(self, *args):
    """Resolves multiple arguments at once and returns their values as a tuple in the order they
    were specified.
    """
    return (self.resolve(arg) for arg in args)

  def _resolve_function(self, arg):
    """Resolves a function instruction."""
    _, signature, fn_args, position = arg
    fn = self.scope.get_function(signature)
    try:
      return fn(self, *fn_args)
    except FunctionError as ex:
      raise RuntimeError(position, str(ex))
    except TypeError as ex:
      raise RuntimeError(position, str(ex))

  def _resolve_variable(self, arg, *, none_ok=False):
    """Resolves a variable instruction."""
    _, name, position = arg
    try:
      raw_value = self.scope.get_variable(name)
    except ScopeError as ex:
      raise RuntimeError(position, str(ex))

    value = self.resolve(raw_value, none_ok=none_ok)
    if value != raw_value:
      self.scope.overwrite_variable(name, value)
    return value

  def _resolve_value(self, arg):
    """Resolves a value instruction."""
    _, vtype, vstr = arg
    if vtype == "Number":
      return Decimal(vstr)
    elif vtype == "String":
      return vstr
    elif vtype == "Boolean":
      return vstr == "True"
    else:
      raise Exception("Unknown value type: {0}".format(vtype))

  def _resolve_branch(self, arg):
    _, options, position = arg
    for option in options:
      passes, val = self._resolve_branch_option(option)
      if passes:
        return val
    raise RuntimeError(position, "Non-exhaustive branch")

  def _resolve_branch_option(self, arg):
    _, result, pred = arg
    if pred is None or self.resolve(pred) == True:
      return (True, self.resolve(result))
    return (False, None)

  def _resolve_switch(self, arg):
    _, subj, cases, position = arg
    subject = self.resolve(subj)
    for case in cases:
      _, result, comparison = case
      if comparison is None or self.resolve(comparison) == subject:
        return self.resolve(result)
    raise RuntimeError(position, "Non-exhaustive switch")
