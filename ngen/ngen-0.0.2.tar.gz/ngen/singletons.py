import six
from functools import wraps
from threading import Lock


class SingletonBase(type):

    def __new__(cls, name, bases, attrs):
        new_class = super(SingletonBase, cls).__new__(cls, name, bases, attrs)
        parents = [base for base in bases if isinstance(base, SingletonBase)]
        if parents:
            new_class._instance = None
        return new_class


class WeakSingleton(six.with_metaclass(SingletonBase)):
    """
        Allows the singleton pattern to be inherited in the usual python style:
            class A(WeakSingleton):
                pass

            class B(WeakSingleton):
                pass

            a0 = A()
            a1 = A()
            a0 is a1  # True

            b = B()
            b is A()  # False
        It also exposes a setUp method on the instance level which can be used
        to characterize the singleton.
    """

    _instance = None
    _mutex = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
            cls._mutex = Lock()
            cls._instance.setUp()
        return cls._instance

    def setUp(self):
        """
            setUp is run once and once only when instantiating the Singleton
            class. Override the function to attach attributes to the singleton
            object.
        """
        pass

    @property
    def lock(self):
        return self._mutex

    def reset(self):
        self.setUp()


class StrongSingleton(object):
    """
        Does not allow inheritance in the commonly understood python fashion.
        Once instantiated all subclasses of the StrongSingleton will reference
        the same object.
    """

    # the __ i.e. dunder mangles the attribute name on the class and as such
    # all subclasses will have _StongSingleton__instance as the reference to
    # singleton object.
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
            cls.__instance.setUp()
        return cls.__instance

    def setUp(self):
        pass

    def reset(self):
        self.setUp()

    @classmethod
    def _clear(cls):
        cls.__instance = None


Singleton = WeakSingleton
SingletonPrime = StrongSingleton


def lock(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        with self.lock:
            ret = func(self, *args, **kwargs)
        return ret
    return wrapper
