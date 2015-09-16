"""This module contains classes and methods for working with scopes in PXP programs. Scopes are
collections of variables, constants and functions that programs can refer to.
"""

from contextlib import contextmanager

from pxp.exception import ScopeError
from pxp.function import FunctionList


class ScopeBase(object):
  """The base class for all Scope classes. This class is abstract."""
  def __init__(self):
    """Initialize the ScopeBase instance."""
    pass

  def contains_variable(self, name):
    """Returns True if the scope contains a variable or constant matching the given name."""
    raise NotImplementedError()

  def is_constant(self, name):
    """Returns True if the scope contains a constant matching the given name."""
    raise NotImplementedError()

  def get_variable(self, name):
    """Returns the value registered for a variable or constant in the scope."""
    raise NotImplementedError()

  def set_variable(self, name, value):
    """Sets the value of a variable in the scope."""
    raise NotImplementedError()

  def overwrite_variable(self, name, value):
    """Overwrite the value of a variable in the scope."""
    raise NotImplementedError()

  def contains_function(self, signature):
    """Returns True if the scope contains the function with the given signature."""
    raise NotImplementedError()

  def get_function(self, signature):
    """Returns the Function object registered with the given signature."""
    raise NotImplementedError()


class DictScope(ScopeBase):
  """A subclass of ScopeBase that contains the variables and constants in a python dictionary."""
  def __init__(self, variables=None, constants=None, functions=None):
    """Construct the DictScope instance."""
    super().__init__()
    self.variables = variables or {}
    self.constants = constants or {}
    self.functions = functions or FunctionList()

  def contains_variable(self, name):
    """Returns True if the scope contains a variable or constant matching the given name."""
    return name in self.variables or self.is_constant(name)

  def is_constant(self, name):
    """Returns True if the scope contains a constant matching the given name."""
    return name in self.constants

  def get_variable(self, name):
    """Returns the variable or constant with the given name. If the scope contains both a
    variable and a constant with the given name, the variable is returned. If no variable or
    constant with the given name is found, a ScopeError is raised.
    """
    if name in self.variables:
      return self.variables[name]
    elif self.is_constant(name):
      return self.constants[name]
    else:
      raise ScopeError("Unknown variable or constant {0}".format(name))

  def set_variable(self, name, value):
    """Sets the value of the variable. If a constant is registered with the given name, a
    ScopeError is raised.
    """
    if self.is_constant(name):
      raise ScopeError("Cannot redefine constant {0}".format(name))
    else:
      self.variables[name] = value

  def overwrite_variable(self, name, value):
    """Passes through to set_veriable."""
    self.set_variable(name, value)

  def contains_function(self, signature):
    """Returns True if a function has been registered with the scope with the given signature."""
    return signature in self.functions

  def get_function(self, signature):
    """Returns the function registered with the given signature."""
    return self.functions[signature]


class ScopeStack(ScopeBase):
  """A scope stack is a specialization of ScopeBase that contains a stack of scopes, and will
  search through them from top to bottom looking for variables and functions.
  """
  def __init__(self, *scopes):
    """Initialize the ScopeStack instance."""
    super().__init__()
    self.scopes = list(scopes)

  @property
  def current_scope(self):
    """The current (top-most) scope."""
    return self.scopes[-1]

  def contains_variable(self, name):
    """Searches through all scopes from top to bottom for a variable or constant with the given
    name, returning True if one is found.
    """
    for scope in reversed(self.scopes):
      if scope.contains_variable(name):
        return True
    return False

  def is_constant(self, name):
    """Searches through all scopes from top to bottom for a constant with the given name, returning
    True if one is found."""
    for scope in reversed(self.scopes):
      if scope.contains_variable(name):
        return scope.is_constant(name)
    return False

  def get_variable(self, name):
    """Searches through all scopes from top to bottom and returns the first variable or constant
    found in one of the scopes.
    """
    for scope in reversed(self.scopes):
      if scope.contains_variable(name):
        return scope.get_variable(name)
    raise ScopeError("Undefined variable {0}".format(name))

  def set_variable(self, name, value):
    """Sets the value of the variable in current_scope."""
    self.current_scope.set_variable(name, value)

  def overwrite_variable(self, name, value):
    """Searches through alls copes from top to bottom and finds the first the contains variable, and
    overwrites the value.
    """
    for scope in reversed(self.scopes):
      if scope.contains_variable(name):
        scope.set_variable(name, value)
        break
    else:
      raise ScopeError("Undefined variable {0}".format(name))

  def contains_function(self, signature):
    """Searches through all scopes from top to bottom and for a function matching
    """
    for scope in reversed(self.scopes):
      if scope.contains_function(signature):
        return True
    return False

  def get_function(self, signature):
    """Searches through all scopes from top to bottom and returns the first function found that
    matches the given signature.
    """
    for scope in reversed(self.scopes):
      if scope.contains_function(signature):
        return scope.get_function(signature)
    raise ScopeError("Undefined function {0}".format(signature))

  def push(self, scope):
    """Add a scope to the top of the stack."""
    if isinstance(scope, list):
      self.scopes.extend(scope)
    else:
      self.scopes.append(scope)
    return self

  def pop(self, n=1):
    """Pops the current_scope from the stack."""
    return self.scopes.pop()

  @contextmanager
  def using(self, scope):
    """A context manager that adds a scope, executes the code block, and pops the scope off the
    stack.
    """
    self.push(scope)
    try:
      yield self
    finally:
      self.pop()
