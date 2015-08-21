# -*- coding: utf-8 -*-
from _common import M2mMapping
from collections import MutableMapping
from util import parse
from copy import deepcopy

__author__ = 'dengjing'


class m2mdict(M2mMapping, MutableMapping):
    def __iter__(self):
        for k, v in self._bmap.items():
            yield k, v

    def __delitem__(self, key):
        del self._fmap[key]

    def items(self):
        return self._fmap.items()

    def keys(self):
        ks = []
        for k, v in self.items():
            ks.append(k)
        return ks

    def __setitem__(self, key, value):
        self._fmap[key] = value

    def getdefault(self, key):
        return self._fmap[key][0]

    def setdefault(self, key, value):
        if isinstance(self._fmap[key], list):
            if value in self._fmap[key]:
                self._fmap[key].insert(0, (self._fmap.pop(self._fmap[key].index(value))))
            else:
                self._fmap[key].insert(0, value)
        else:
            if key not in self.keys():
                self._fmap[key] = [value]
            else:
                raise Exception('the value expect a base.')


if __name__ == '__main__':
    d = m2mdict([("img/x-jpeg", "jpg"), ("img/jpeg", "jpg"), ("img/jpeg", "jepg")])
    print(d.items())
    print(d.getdefault('img/jpeg'))
    # print ~d
    d.setdefault('img/jpeg', 'jpeg')
    print(d.getdefault('img/jpeg'))