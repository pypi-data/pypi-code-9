import functools
from collections import MutableMapping

from .utils import *

__all__ = ['PlutResource']


def validate_name(f):
    @functools.wraps(f)
    def _(self, name, *a, **kw):
        if not check_name(name):
            raise NameError('name should contain uppercase letters only')
        return f(self, name, *a, **kw)
    return _


class PlutResource(MutableMapping):
    def __init__(self, filename=None):
        if filename is None:
            filename = os.path.expanduser('~/.plutrc')

        self.filename = filename
        self.rc = read_resource(filename)

    def save(self):
        save_resource(self.rc, self.filename)

    @validate_name
    def __getitem__(self, name):
        return self.rc[name]

    @validate_name
    def __setitem__(self, name, port):
        self.rc[name] = int(port)
        self.save()

    @validate_name
    def __delitem__(self, name):
        del self.rc[name]
        self.save()

    def __iter__(self):
        return iter(self.rc)

    @validate_name
    def __contains__(self, name):
        return name in self.rc

    def __len__(self):
        return len(self.rc)
