from importlib import import_module
import os
import json


# TODO: pandas can also read in JSON easily
# TODO: an `objects` loader that parses the CSV or JSON
# but does not read it into a Pandas DataFrame
class CSVLoader(object):
    def __init__(self, root=None):
        self.root = root or os.getcwd()

    def __getattr__(self, name):
        dirpath = os.path.join(self.root, name)
        filepath = dirpath + '.csv'

        if os.path.exists(filepath):
            import pandas
            data = pandas.read_table(filepath, sep=',')
            setattr(self, name, data)
            return data
        elif os.path.isdir(dirpath):
            return self.__class__(dirpath)
        else:
            root = os.getcwd()
            raise IOError('Dataset {name}.csv not found in {directory}.'.format(
                name=name,
                directory=root,
                ))

    """
    Not sure yet what a non-insane way of persisting new/modified datasets would be,
    and if it's even necessary, but might be interesting to play around with.

    E.g.

        tables.modif = tables.test.apply(...)
        tables.save()

    `setattr` puts files on a "to save" list, and then calling save does the
    final persistence.
    """
    #def __setattr__(self):
    #    raise NotImplementedError()

    #def save(self):
    #    raise NotImplementedError()


tables = CSVLoader()


def here(*segments):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), *segments)


helpers = json.load(open(here('helpers.json')))


class LazyVariable(object):
    triggers = {}

    def __init__(self, package, name, representation):
        self.package = package
        self.name = name
        self.representation = representation

    @property
    def value(self):
        g = globals()
        module = import_module(self.package)
        g.update(module.__dict__)
        g[self.package] = module

        if self.package in self.triggers:
            g.update(self.triggers[self.package](module))

        if self.name:
            return g[self.name]
        else:
            return module

    def __repr__(self):
        return self.representation

    def __getattr__(self, name):
        return getattr(self.value, name)

    def __invert__(self):
        return -self.value

    def __add__(self, other):
        return self.value + other

    def __radd__(self, other):
        return self.value + other

    def __sub__(self, other):
        return self.value - other

    def __rsub__(self, other):
        return other - self.value

    def __mul__(self, other):
        return self.value * other

    def __rmul__(self, other):
        return self.value * other

    def __truediv__(self, other):
        return self.value / other

    def __rtruediv__(self, other):
        return other / self.value

    def __pow__(self, other):
        return self.value ** other

    def __rpow__(self, other):
        return other ** self.value

    def __call__(self, *vargs, **kwargs):
        return self.value(*vargs, **kwargs)


def __sympy(module):
    """
    * f, g, h are often reserved for functions
    * i, j, k, l, m, n are often indices
    * t is the t distribution

    ... but everything else is nice to have defined out of the box
    """

    keys = 'a b c d e o p q r s u v w x y z'
    return dict(list(zip(keys.split(), module.symbols(keys))))


LazyVariable.triggers = {
    'sympy': __sympy,
    }


for package, key, representation in helpers:
    name = key or package
    globals()[name] = LazyVariable(package, key, representation)


# builtin modules generally load fast (there at the top of the list of paths to check), 
# so we don't need to lazyload these
import math
from math import *

import random
from random import *