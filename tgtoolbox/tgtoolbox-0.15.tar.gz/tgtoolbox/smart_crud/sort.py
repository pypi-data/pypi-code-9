# -*- coding: utf-8 -*-
from tg import request
from collections import OrderedDict
__author__ = 'vahid'

class SortItem(object):
    def __init__(self, name, descending=False):
        self.name = name
        self.desc = descending

    @classmethod
    def parse(cls, str):
        return cls(str[1:], descending=str[0] == '-')

    def clone(self):
        return self.__class__(self.name, self.desc)

    def __unicode__(self):
        return U'%s%s' % (u'-' if self.desc else u'+', self.name)

class Sort(object):

    def __init__(self, sort_items=None):
        self.items = OrderedDict()
        if sort_items:
            for item in sort_items:
                self.items[item.name] = item

    def add(self, col_name, descending=False):
        self.items[col_name] = SortItem(col_name, descending)

    def add_or_toggle(self, col_name):
        if col_name in self.items:
            self.items[col_name].desc ^= True
        else:
            self.add(col_name)

    def __iter__(self):
        return iter(self.items.values())

    @classmethod
    def parse(cls, str):
        if not str:
            return cls()
        return cls([SortItem.parse(i) for i in str.split('|')])

    @classmethod
    def from_request(cls):
        return cls.parse(request.GET.get('sort_cols'))

    def __unicode__(self):
        return u'|'.join([unicode(i) for i in self.items.values()])

    def __len__(self):
        return len(self.items)

    def clone(self):
        return self.__class__([i.clone() for i in self.items.values()])

    def get(self, key, default=None):
        return self.items.get(key, default)

    def remove(self, col_name):
        del self.items[col_name]