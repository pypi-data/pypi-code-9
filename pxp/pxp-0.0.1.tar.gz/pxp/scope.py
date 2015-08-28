from contextlib import contextmanager

from pxp.exception import ScopeError
from pxp.function import FunctionList


class ScopeBase(object):
  def __init__(self):
    pass

  def contains_variable(self, name):
    raise NotImplementedError()

  def is_constant(self, name):
    raise NotImplementedError()

  def get_variable(self, name):
    raise NotImplementedError()

  def set_variable(self, name, value):
    raise NotImplementedError()

  def overwrite_variable(self, name, value):
    raise NotImplementedError()

  def contains_function(self, name):
    raise NotImplementedError()

  def get_function(self, signature):
    raise NotImplementedError()


class DictScope(ScopeBase):
  def __init__(self, variables=None, constants=None, functions=None):
    super().__init__()
    self.variables = variables or {}
    self.constants = constants or {}
    self.functions = functions or FunctionList()

  def contains_variable(self, name):
    return name in self.variables or self.is_constant(name)

  def is_constant(self, name):
    return name in self.constants

  def get_variable(self, name):
    # return self.variables[name]
    if name in self.variables:
      return self.variables[name]
    elif self.is_constant(name):
      return self.constants[name]
    else:
      raise ScopeError("Unknown variable or constant {0}".format(name))

  def set_variable(self, name, value):
    if self.is_constant(name):
      raise ScopeError("Cannot redefine constant {0}".format(name))
    else:
      self.variables[name] = value

  def overwrite_variable(self, name, value):
    self.set_variable(name, value)

  def contains_function(self, signature):
    return signature in self.functions

  def get_function(self, signature):
    return self.functions[signature]


class ScopeStack(ScopeBase):
  def __init__(self, *scopes):
    super().__init__()
    self.scopes = list(scopes)

  @property
  def current_scope(self):
    return self.scopes[-1]

  def contains_variable(self, name):
    for scope in reversed(self.scopes):
      if scope.contains_variable(name):
        return True
    return False

  def is_constant(self, name):
    for scope in reversed(self.scopes):
      if scope.contains_variable(name):
        return scope.is_constant(name)
    return False

  def get_variable(self, name):
    for scope in reversed(self.scopes):
      if scope.contains_variable(name):
        return scope.get_variable(name)
    raise ScopeError("Undefined variable {0}".format(name))

  def set_variable(self, name, value):
    self.current_scope.set_variable(name, value)

  def overwrite_variable(self, name, value):
    for scope in reversed(self.scopes):
      if scope.contains_variable(name):
        scope.set_variable(name, value)
        break
    else:
      raise ScopeError("Undefined variable {0}".format(name))

  def contains_function(self, signature):
    for scope in reversed(self.scopes):
      if scope.contains_function(signature):
        return True
    return False

  def get_function(self, signature):
    for scope in reversed(self.scopes):
      if scope.contains_function(signature):
        return scope.get_function(signature)
    raise ScopeError("Undefined function {0}".format(signature))

  def push(self, scope):
    self.scopes.append(scope)
    return self

  def pop(self):
    return self.scopes.pop()

  @contextmanager
  def using(self, scope):
    self.push(scope)
    try:
      yield self
    finally:
      self.pop()
