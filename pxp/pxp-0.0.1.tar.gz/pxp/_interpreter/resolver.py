from decimal import Decimal

from pxp.exception import FunctionError, RuntimeError, ScopeError


class Resolver(object):
  def __init__(self, scope):
    self.scope = scope

  def resolve(self, arg):
    if isinstance(arg, tuple):
      arg_type = arg[0]
      # NOTE: These are 'magical' string values and aren't strongly tied with the AST module.
      if arg_type == "fn":
        return self._resolve_function(arg)
      elif arg_type == "var":
        return self._resolve_variable(arg)
      elif arg_type == "val":
        return self._resolve_value(arg)
      else:
        raise Exception("Unknown arg type: {0}".format(arg_type))
    else:
      return arg

  def resolve_all(self, *args):
    return (self.resolve(arg) for arg in args)

  def _resolve_function(self, arg):
    _, signature, *fn_args, position = arg
    fn = self.scope.get_function(signature)
    try:
      return fn(self, *fn_args)
    except FunctionError as ex:
      raise RuntimeError(position, str(ex))

  def _resolve_variable(self, arg):
    _, name, position = arg
    try:
      raw_value = self.scope.get_variable(name)
    except ScopeError as ex:
      raise RuntimeError(position, str(ex))

    value = self.resolve(raw_value)
    if value != raw_value:
      self.scope.overwrite_variable(name, value)
    return value

  def _resolve_value(self, arg):
    _, vtype, vstr = arg
    if vtype == "Number":
      return Decimal(vstr)
    elif vtype == "String":
      return vstr
    elif vtype == "Boolean":
      return vstr == "True"
    else:
      raise Exception("Unknown value type: {0}".format(vtype))
