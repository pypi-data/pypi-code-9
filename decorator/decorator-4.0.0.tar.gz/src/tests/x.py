import abc
from documentation import get_length
from functools import singledispatch
import collections as c


@singledispatch
def g(obj):
    raise NotImplementedError(type(obj))

g.register(c.Sized)(lambda obj: obj.__len__())
g.register(c.Set)(lambda obj: "set")
get_length.register(c.Sized)(lambda obj: obj.__len__())
get_length.register(c.Set)(lambda obj: "set")


class O(c.Sized):
    def __len__(self):
        return 0
c.Set.register(O)

print(g(O()))
print(get_length(O()))


class C(metaclass=abc.ABCMeta):
    pass

C.register(O)
