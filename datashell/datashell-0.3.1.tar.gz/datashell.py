from importlib import import_module
import os
import json


PROFILE = 'data'


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

    # Not sure yet what a non-insane way of persisting new/modified datasets would be,
    # and if it's even necessary, but might be interesting to play around with.
    #
    # E.g.
    #
    #     tables.modif = tables.test.apply(...)
    #     tables.save()
    #
    # `setattr` puts files on a "to save" list, and then calling save does the
    # final persistence.
    
    #def __setattr__(self):
    #    raise NotImplementedError()
    
    #def save(self):
    #    raise NotImplementedError()


tables = CSVLoader()


def here(*segments):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), *segments)


helpers = json.load(open(here('profiles/build/{}.json'.format(PROFILE))))


class LazyVariable(object):
    loaded = set()

    def __init__(self, package, name, representation):
        self.package = package
        self.name = name
        self.representation = representation

    # In most cases, when lazy-loading something you'd implement
    # some sort of memoization routine. Here, instead, we replace
    # the lazy variable with its loaded equivalent by directly
    # modifying the global namespace. The lazy variable vanishes
    # as soon as it is called. While perhaps a bit hackish, 
    # in this particular case I feel it's actually the more 
    # robust solution.
    @property
    def value(self):
        g = globals()
        module = import_module(self.package)
        g.update(module.__dict__)
        g[self.package] = module
        self.loaded.add(self.package)

        if self.name:
            return g[self.name]
        else:
            return module

    def __repr__(self):
        return self.representation

    def __getattr__(self, name):
        return getattr(self.value, name)

    def __call__(self, *vargs, **kwargs):
        return self.value(*vargs, **kwargs)

    # All methods that follow are primarily useful in the context of sympy, 
    # to enable e.g. `diff(2**x)` when neither `diff` or `sympy.symbols('x')`
    # is loaded yet.
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


for package, key, representation in helpers:
    name = key or package
    globals()[name] = LazyVariable(package, key, representation)
