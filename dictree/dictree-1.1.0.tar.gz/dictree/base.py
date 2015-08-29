# coding:utf-8

from collections import MutableMapping
from .labels import WILDCARD, NO_ITEM


class Base(MutableMapping):
    def __init__(self):
        self._item = NO_ITEM
        self._subtrees = {}

    def __contains__(self, key):
        if len(key) == 0:
            return self._item is not NO_ITEM

        else:
            head, tail = key[0], key[1:]
            if head in self._subtrees:
                return tail in self._subtrees[head]

            else:
                return False

    def __len__(self):
        n = sum(len(t) for t in self._subtrees.values())
        return n+1 if self._item is not NO_ITEM else n

    def __iter__(self):
        if self._item is not NO_ITEM:
            yield ()

        for head in self._subtrees:
            for tail in self._subtrees[head]:
                yield (head,) + tail

    def __getitem__(self, key):
        return Base.find(self, key, True)[0]

    def __setitem__(self, key, value):
        if len(key) == 0:
            self._item = value

        else:
            head, tail = key[0], key[1:]
            self._subtrees.setdefault(head, self.__class__())[tail] = value

    def __delitem__(self, key):
        if len(key) == 0:
            if self._item is not NO_ITEM:
                self._item = NO_ITEM
                return len(self._subtrees) == 0

            else:
                raise KeyError()

        else:
            head, tail = key[0], key[1:]
            if Base.__delitem__(self._subtrees[head], tail):
                del self._subtrees[head]

            return self._item is NO_ITEM and len(self._subtrees) == 0

    def setdefault(self, key, default):
        if key in self:
            return self[key]

        else:
            self[key] = default
            return default

    def find(self, key, perfect_match):
        if len(key) == 0:
            if self._item is not NO_ITEM:
                return self._item, ()

            else:
                raise KeyError()

        else:
            head, tail = key[0], key[1:]
            try:
                item, trace = Base.find(self._subtrees[head],
                                        tail,
                                        perfect_match)
                return item, (False,) + trace

            except KeyError:
                try:
                    item, trace = Base.find(self._subtrees[WILDCARD],
                                            tail,
                                            perfect_match)
                    return item, (True,) + trace

                except KeyError:
                    if perfect_match:
                        raise KeyError()

                    else:
                        return Base.find(self, (), perfect_match)
