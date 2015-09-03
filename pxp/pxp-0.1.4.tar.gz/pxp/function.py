"""This module contains classes and methods for defining functions that can be called from PXP
programs.
"""

from collections import namedtuple


_Undefined = object()
FunctionArg = namedtuple("FunctionArg", ["type", "name", "default", "description"])
FunctionArg.__new__.__defaults__ = (_Undefined, None)


class Function(object):
  """This is the base class for implementations of PXP functions."""
  def __init__(self, name, args, return_type):
    """Construct the Function instance."""
    self.name = name
    self.args = args
    self.return_type = return_type
    self._signatures = None

  @property
  def signatures(self):
    """Each function has one or more type signatures.

    A type signature is a tuple containing the name of the function, and type types of its
    arguments.

    If a function has any arguments with default values, it will have multiple signatures. E.G.
    if a function takes two Number arguments, the second of which has a default value of 0, it
    would have two signatures:

    (function_name, "Number", "Number"), and
    (function_name, "Number")
    """
    if self._signatures is None:
      args = list(self.args)
      self._signatures = [(self.name, ) + tuple(a.type for a in args)]

      while args and args[-1].default is not _Undefined:
        args = args[:-1]
        self._signatures.append((self.name, ) + tuple(a.type for a in args))
    return self._signatures

  @property
  def doc(self):
    raise NotImplementedError()

  def call(self):
    """The implementation of the function, __call__ builds the argument list and delegates the call
    to this method."""
    raise NotImplementedError()


  def __call__(self, resolver, *args, **kwargs):
    """Given a resolver and args and keywords args, build an argument list to be passed to the
    call method of the class. The args and keyword args are checked against the order and names of
    the class' args list.
    """
    send_args = []
    for i, arg in enumerate(self.args):
      if i < len(args):
        send_args.append(args[i])
      elif arg.name in kwargs:
        send_args.append(kwargs[arg.name])
      else:
        if arg.default is _Undefined:
          raise Exception("No value given for required "
                          "argument {0} in function {1}".format(arg.name,
                                                                self.name))
        else:
          send_args.append(arg.default)
    return self.call(resolver, *send_args)


class InjectedFunction(Function):
  """A subclass of Function that accepts a function which .call delegates to."""
  def __init__(self, name, args, return_type, call):
    """Constructs the InjectedFunction instance."""
    super().__init__(name, args, return_type)
    self._call = call

  @property
  def doc(self):
    return self._call.__doc__

  def call(self, *args):
    """Pass *args to the function given to the constructor."""
    return self._call(*args)


class FunctionList(object):
  """FunctionList is an object that holds a list of functions, registered by their signatures and
  allows the lookup of functions based on their signature.
  """
  def __init__(self, registrants=None):
    """Constructs the FunctionList instance."""
    self.functions = {}
    if registrants:
      for function in registrants:
        self.register(function)

  def __contains__(self, signature):
    """Returns True if the given signature matches one of the registered functions."""
    return signature in self.functions

  def __getitem__(self, signature):
    """Returns the function registered under signature."""
    return self.functions[signature]

  def __setitem__(self, signature, function):
    """Registers a function with signature."""
    if signature in self:
      raise Exception("Redefinition of function {0}".format(signature))
    else:
      self.functions[signature] = function

  def register(self, function):
    """Register a function. Iterates through all the function's signatures and registers the
    function under each.
    """
    for signature in function.signatures:
      self[signature] = function
    return self

  def merge(self, *others):
    """Merge other function lists into this instance.

    Each argument can be either a FunctionList, a list, or a tuple.

    If the argument is a list or tuple, each item is expected to be a Function instance and the
    functions are passed to register.
    """
    for other in others:
      if isinstance(other, (list, tuple)):
        for fxn in other:
          self.register(fxn)
      elif isinstance(other, FunctionList):
        for sig, fxn in other.functions.items():
          self[sig] = fxn
    return self
