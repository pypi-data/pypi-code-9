from functools import wraps, update_wrapper

from .kfij import Kfij

class List(Kfij):
    factory = list
    def load(self):
        self.extend(self.readlines())
    def dump(self):
        self.writelines(self)

    @wraps(list.append)
    def append(self, x):
        self.writelines([x])
        self.cache.append(x)

    @wraps(list.extend)
    def extend(self, iterable):
        for x in iterable:
            self.append(x)

    __iadd__ = append
    update_wrapper(__iadd__, list.__iadd__)

List.enable_safe_funcs('copy', 'count', 'index',
    '__add__', '__ge__', '__le__', '__len__', '__rmul__',
    '__contains__', '__getitem__', '__lt__',
    '__gt__', '__mul__', 
    '__reversed__',
    '__hash__', '__ne__',
    '__str__',
    '__eq__',
    '__format__', '__iter__', '__repr__')


List.enable_destructive_funcs('insert', 'remove', 'sort', 'clear', 'pop', 'reverse',
                              '__setitem__', '__delitem__', '__imul__', '__iadd__')
