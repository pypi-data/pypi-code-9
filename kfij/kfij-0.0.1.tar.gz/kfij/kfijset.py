from functools import wraps

from .kfij import Kfij

class Set(Kfij):
    factory = set
    def load(self):
        self.update(self.readlines())
    def dump(self):
        self.writelines(self)

    @wraps(set.add)
    def add(self, x):
        # Filter
        if x not in self.cache:
            self.writelines([x])
            self.cache.add(x)

    @wraps(set.update)
    def update(self, iterable):
        for x in iterable:
            self.add(x)

Set.enable_safe_funcs('copy', 'isdisjoint', 'issubset',
                      'difference', 'union', 'intersection', 'symmetric_difference',
                      '__repr__', '__str__',
                      '__contains__', '__len__', '__iter__',
                      '__sub__', '__rsub__',
                      '__and__', '__or__',
                      '__rand__', '__ror__', '__rxor__',
                      '__ge__', '__gt__', '__le__', '__lt__', '__eq__')
Set.enable_destructive_funcs('clear', 'pop', 'remove',
                             'intersection_update',
                             'symmetric_difference_update',
                             'update')
