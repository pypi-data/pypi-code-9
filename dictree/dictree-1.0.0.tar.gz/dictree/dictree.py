# coding:utf-8

from collections import MutableMapping
from .labels import Wildcard, NoItem


class Dictree(MutableMapping):
    WILDCARD = Wildcard()
    _NO_ITEM = NoItem()

    def __init__(self):
        self._item = self._NO_ITEM
        self._subtrees = {}

    @property
    def item(self):
        return self._item

    @item.setter
    def item(self, value):
        self._item = value

    @item.deleter
    def item(self):
        self._item = self._NO_ITEM

    @property
    def has_item(self):
        return self.item is not self._NO_ITEM

    @property
    def has_subtree(self):
        return len(self._subtrees) != 0

    @property
    def has_wildcard(self):
        return self.WILDCARD in self._subtrees

    def __len__(self):
        n = sum(len(t) for t in self._subtrees.values())
        return n + 1 if self.has_item else n

    def __iter__(self):
        if self.has_item:
            yield ()

        for k, t in self._subtrees.items():
            for l in t:
                yield (k,) + l

    def __contains__(self, key):
        if len(key) == 0:
            return self.has_item

        else:
            head, tail = key[0], key[1:]
            if head in self._subtrees:
                return tail in self._subtrees[head]

            else:
                return False

    def __getitem__(self, key):
        if len(key) == 0:
            if self.has_item:
                return self.item

            else:
                raise KeyError(key)

        else:
            head, tail = key[0], key[1:]
            if head in self._subtrees:
                try:
                    return self._subtrees[head][tail]

                except KeyError:
                    try:
                        return self._subtrees[self.WILDCARD][tail]

                    except KeyError:
                        raise KeyError(key)

            elif self.has_wildcard:
                try:
                    return self._subtrees[self.WILDCARD][tail]

                except KeyError:
                    raise KeyError(key)

            else:
                raise KeyError(key)

    def __setitem__(self, key, item):
        if len(key) == 0:
            self.item = item

        else:
            head, tail = key[0], key[1:]
            self._subtrees.setdefault(head, self.__class__())[tail] = item

    def __delitem__(self, key):
        if len(key) == 0:
            if self.has_item:
                del self.item
                return not self.has_subtree

            else:
                raise KeyError(key)

        else:
            head, tail = key[0], key[1:]
            if head in self._subtrees:
                try:
                    become_empty = self._subtrees[head].__delitem__(tail)

                except KeyError:
                    raise KeyError(key)

                else:
                    if become_empty:
                        del self._subtrees[head]

                    return not self.has_subtree and not self.has_item

            else:
                raise KeyError(key)

    def setdefault(self, key, default):
        if key in self:
            return self[key]

        else:
            self[key] = default
            return default

    def find(self, key):
        if len(key) == 0:
            if self.has_item:
                return self.item, ()

            else:
                raise KeyError(key)

        else:
            head, tail = key[0], key[1:]
            if head in self._subtrees:
                try:
                    item, trace = self._subtrees[head].find(tail)
                    return item, (False,) + trace

                except KeyError:
                    try:
                        item, trace = self._subtrees[self.WILDCARD].find(tail)
                        return item, (True,) + trace

                    except KeyError:
                        try:
                            return self.find(())

                        except KeyError:
                            raise KeyError(key)

            elif self.has_wildcard:
                try:
                    item, trace = self._subtrees[self.WILDCARD].find(tail)
                    return item, (True,) + trace

                except KeyError:
                    try:
                        return self.find(())

                    except KeyError:
                        raise KeyError(key)

            else:
                try:
                    return self.find(())

                except KeyError:
                    raise KeyError(key)
