import functools
from collections import MutableMapping

from .utils import *
import config

__all__ = ['PlutResource']


class PlutResource(MutableMapping):
    def __init__(self):
        self.rc = read_resource(config.rcfile)

    def save(self):
        save_resource(self.rc, config.rcfile)

    def __getitem__(self, name):
        return self.rc[name]

    def __setitem__(self, name, port):
        self.rc[name] = int(port)
        self.save()

    def __delitem__(self, name):
        del self.rc[name]
        self.save()

    def __iter__(self):
        return iter(self.rc)

    def __contains__(self, name):
        return name in self.rc

    def __len__(self):
        return len(self.rc)
