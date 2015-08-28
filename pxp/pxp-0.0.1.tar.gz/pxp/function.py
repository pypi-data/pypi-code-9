from collections import namedtuple


_Undefined = object()
FunctionArg = namedtuple("FunctionArg", ["type", "name", "default"])
FunctionArg.__new__.__defaults__ = (_Undefined, )


class Function(object):
  def __init__(self, name, args, return_type):
    self.name = name
    self.args = args
    self.return_type = return_type
    self._signatures = None

  @property
  def signatures(self):
    if self._signatures is None:
      args = list(self.args)
      self._signatures = [(self.name, ) + tuple(a.type for a in args)]

      while args and args[-1].default is not _Undefined:
        args = args[:-1]
        self._signatures.append((self.name, ) + tuple(a.type for a in args))
    return self._signatures

  def __call__(self, resolver, *args, **kwargs):
    send_args = []
    for i, arg in enumerate(self.args):
      if i < len(args):
        send_args.append(args[i])
      elif arg.name in kwargs:
        send_args.append(kwargs[arg.name])
      else:
        if arg.default is _Undefined:
          raise Exception("No value given for required argument {0} in function {1}".format(arg.name, self.name))
        else:
          send_args.append(arg.default)
    return self.call(resolver, *send_args)

  def call(self):
    raise NotImplementedError()


class InjectedFunction(Function):
  def __init__(self, name, args, return_type, call):
    super().__init__(name, args, return_type)
    self._call = call

  def call(self, *args):
    return self._call(*args)


class FunctionList(object):
  def __init__(self, registrants=None):
    self.functions = {}
    if registrants:
      for function in registrants:
        self.register(function)

  def __contains__(self, signature):
    return signature in self.functions

  def __getitem__(self, signature):
    return self.functions[signature]

  def __setitem__(self, signature, function):
    if signature in self:
      raise Exception("Redefinition of function {0}".format(signature))
    else:
      self.functions[signature] = function

  def register(self, function):
    for signature in function.signatures:
      self[signature] = function
    return self

  def merge(self, *others):
    for other in others:
      if isinstance(other, (list, tuple)):
        for fxn in other:
          self.register(fxn)
      elif isinstance(other, FunctionList):
        for sig, fxn in other.functions.items():
          self[sig] = fxn
    return self
