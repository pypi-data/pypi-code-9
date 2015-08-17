# -*- coding: utf-8 -*-
from _common import M2mMapping
from collections import MutableMapping
from util import parse
from copy import deepcopy

__author__ = 'dengjing'


class m2mdict(M2mMapping, MutableMapping):
    def __delitem__(self, key):
        if not self._rflag:
            count = 0
            raw = deepcopy(self._rawmap)
            for (k, v) in raw:
                if k == key:
                    self._rawmap.remove((k, v))
                    count += 1
            if count > 0:
                self._bmap = parse([self._rawmap], True)
                self._fmap = parse([self._rawmap], False)
        else:
            count = 0
            raw = deepcopy(self._rawmap)
            for (k, v) in raw:
                if v == key:
                    self._rawmap.remove((k, v))
                    count += 1
            if count > 0:
                self._bmap = parse([self._rawmap], True)
                self._fmap = parse([self._rawmap], False)

    def delitem(self, key):
        count = 0
        raw = deepcopy(self._rawmap)
        for (k, v) in raw:
            if k == key or v == key:
                self._rawmap.remove((k, v))
                count += 1
        if count > 0:
            self._bmap = parse([self._rawmap], True)
            self._fmap = parse([self._rawmap], False)
        else:
            raise TypeError('the key isn`t exist.')

    def add(self, key, value):
        if isinstance(value, set):
            if not self._rflag:
                for i in value:
                    self._rawmap.append((key, i))
            else:
                for i in value:
                    self._rawmap.append((i, key))
            self._bmap = parse([self._rawmap], True)
            self._fmap = parse([self._rawmap], False)
        else:
            raise TypeError('the args isn`t right.')

    def __iter__(self):
        if self._rflag:
            for k, v in self._bmap.items():
                yield k, v
        else:
            for k, v in self._fmap.items():
                yield k, v

    def items(self):
        if self._rflag:
            return self._bmap.items()
        else:
            return self._fmap.items()

    def keys(self):
        ks = []
        for k, v in self.items():
            ks.append(k)
        return ks

    def clear(self):
        self._rawmap = []
        self._bmap.clear()
        self._fmap.clear()

    def __setitem__(self, key, value):
        del self[key]
        self.add(key, value)

    def getdefault(self, key):
        if not self._rflag:
            if key in self.keys():
                v = self[key]
                if len(v) == 1:
                    return list(v)[0]
                else:
                    if self.rdefault[key]:
                        return self.rdefault[key]
                    else:
                        raise ValueError('the default value isn`t found')
            else:
                raise KeyError('the key isn`t exist.')
        else:
            if key in self.keys():
                v = self[key]
                if len(v) == 1:
                    return list(v)[0]
                else:
                    if self.ldefault[key]:
                        return self.ldefault[key]
                    else:
                        raise ValueError('the default value isn`t found')
            else:
                raise KeyError('the key isn`t exist.')

    def setdefault(self, key, value):
        if not self._rflag:
            self.rdefault[key] = value
            self.ldefault[value] = key
        else:
            self.rdefault[value] = key
            self.ldefault[key] = value
        self.add(key, {value})


if __name__ == '__main__':
    pass