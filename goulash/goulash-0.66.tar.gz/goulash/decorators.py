""" goulash.decorators
"""
import inspect
from goulash._fabric import require_bin
# SOURCE:
#  http://code.activestate.com/recipes/578852-decorator-to-check-if-needed-modules-for-method-ar/


class require_module(object):

    """ """

    def __init__(self, names, msg=None):
        if isinstance(names, (str, unicode)):
            self.names = [names]
        else:
            self.names = names
        self.msg = msg

    def __call__(self, f):
        self.f = f
        return self.wrapped

    def wrapped(self, *args, **kargs):
        for name in self.names:
            try:
                __import__(name)
            except ImportError:
                if self.msg is None:
                    self.msg = ('{0} requires {1}.  Try running '
                                '"pip install {1}" before you continue').format(
                        self.f.__name__,
                        name)
                raise ImportError(self.msg)
        return self.f(*args, **kargs)


class arg_types(object):

    """ A decorator which enforces the rule that all arguments must be
        of type .  All keyword arguments are ignored. Throws ArgTypeError
        when expectations are violated.

        Example usage follows:

          @arg_types(int, float)
          def sum(*args): pass
    """

    class ArgTypeError(TypeError):
        pass

    def __init__(self, *args):
        err = 'all arguments to arg_types() should be types, got {0}'
        assert all([inspect.isclass(a) for a in args]), err.format(args)
        self.types = args

    def __call__(self, fxn):
        self.fxn = fxn

        def wrapped(*args, **kargs):
            for a in args:
                if not isinstance(a, self.types):
                    raise self.ArgTypeError(
                        "{0} (type={1}) is not in {2}".format(
                            a, type(a), self.types))
            return self.fxn(*args, **kargs)
        return wrapped

# SOURCE:
#   http://www.reddit.com/r/Python/comments/ejp25/cached_property_decorator_that_is_memory_friendly/


class memoized_property(object):

    """ A read-only @property that is only evaluated once. """

    def __init__(self, fget, doc=None):
        self.fget = fget
        self.__doc__ = doc or fget.__doc__
        self.__name__ = fget.__name__

    def __get__(self, obj, cls):
        if obj is None:
            return self
        obj.__dict__[self.__name__] = result = self.fget(obj)
        return result

# SOURCE:
#  http://stackoverflow.com/questions/128573/using-property-on-classmethods


class classproperty(property):

    """
        USAGE:
          class constants:
              @classproperty
              def lazy(kls):
                  return "whatevs"
    """

    def __init__(self, func):
        return super(classproperty, self).__init__(classmethod(func))

    def __get__(self, obj, type_):
        return self.fget.__get__(None, type_)()

    def __set__(self, obj, value):
        cls = type(obj)
        return self.fset.__get__(None, cls)(value)
