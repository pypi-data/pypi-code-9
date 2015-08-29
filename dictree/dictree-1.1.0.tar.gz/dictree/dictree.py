# coding:utf-8

from .base import Base


class Dictree(Base):
    def __getitem__(self, key):
        try:
            return super(Dictree, self).__getitem__(key)

        except KeyError:
            raise KeyError(key)

    def __delitem__(self, key):
        try:
            super(Dictree, self).__delitem__(key)

        except KeyError:
            raise KeyError(key)

    def find(self, key, perfect_match=False):
        try:
            return super(Dictree, self).find(key, perfect_match)

        except KeyError:
            raise KeyError(key)
