#!/usr/bin/env python

from tinydb import TinyDB, where

DB_PATH = './abyss_db.json'
DB = TinyDB(DB_PATH)

def deserialize(serialized):
    module = __import__(serialized['_module'])
    for modattr in serialized['_module'].split('.')[1:]:
        module = getattr(module, modattr)
    cls = getattr(module, serialized['_type'])
    obj = cls.deserialize(**serialized)
    obj.eid = getattr(serialized, 'eid', None)
    return obj

def serialize(obj):
    return obj._serialize()

class stored(object):

    def _serialize(self):
        data = {
            '_type': self.__class__.__name__,
            '_module': self.__class__.__module__,
        }
        data.update(self.serialize())
        return data

    def serialize(self):
        return {
            attr: getattr(self, attr) 
            for attr in self.__slots__
        }

    @classmethod
    def deserialize(cls, **kwargs):
        return cls(**kwargs)

    def store(self):
        table = DB.table(self.__class__.__name__)
        d = self._serialize()
        if not hasattr(self, 'eid'):
            self.eid = table.insert(d)
        else:
            table.update(d, eids=[self.eid])

class Test(stored):
    __slots__ = ('foo', 'bar')

    def __init__(self, foo=None, bar=None, **kwargs):
        self.foo = foo
        self.bar = bar
