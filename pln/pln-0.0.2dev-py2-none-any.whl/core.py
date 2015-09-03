"""Apply successive operations on your data"""


from functools import wraps, partial


class Watch(object):
    """A watch just print the value passed to it then returns it

    It's very handy when it is used in a pipeline.

    >>> p = Pipeline(2)
    >>> inc = lambda x: x + 1
    >>> watch = Watch()

    >>> p >> inc >> watch >> str >> watch
    Result 1: 3
    Pipeline('3')
    Result 2: '3'

    Note: a `Watch` instance should be used only for a single data
    otherwise the counter will be incorrect.
    """
    def __init__(self):
        self.data = None
        self.counter = 0

    def __call__(self, data):
        self.counter += 1
        self.data = data
        print "Result %d: %r" % (self.counter, self.data)
        return self.data

    def __str__(self):
        return "<Watch: %d operations>" % self.counter

    __repr__ = __str__


def shift(func, *args, **kwargs):
    """This function is basically a beefed up lambda x: func(x, *args, **kwargs)

    `shift` comes in handy when it is used in a pipeline with a function that
    needs the passed value as its first argument.

    >>> p = Pipeline(42)
    >>> def div(x, y): return float(x) / y

    # This is equivalent to div(42, 2):
    >>> shift(div, 2)(42)
    21

    # which is different from div(2, 42):
    >>> partial(div, 2)(42)
    0.047619047619047616

    """
    @wraps(func)
    def wrapped(x):
        return func(x, *args, **kwargs)
    return wrapped


class Pipeline(object):
    """A class to apply successive operations on data with a simple syntax

    >>> p = Pipeline(2)
    >>> inc = lambda x: x + 1

    >>> p >> inc >> str
    Pipeline('3')

    """
    def __init__(self, value):
        self.value = value

    def __rshift__(self, func):
        return Pipeline(func(self.value))

    def __str__(self):
        return "%s(%r)" % (self.__class__.__name__, self.value)

    __repr__ = __str__
