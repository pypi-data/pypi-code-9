#!/usr/bin/env python
''' abyss.entity '''
from abyss.account import User

class owned(stored):
    
    def serialize(self):
        d = {}
        for attr in self.__slots__:
            if attr == 'owner':
                val = self.owner.username if self.owner else None
            else:
                val = getattr(self, attr)
            d[attr] = val
        return d

    @classmethod
    def deserialize(cls, **kwargs):
        kwargs_fixed = {}
        for k, v in kwargs.items():
            if k == 'owner':
                kwargs_fixed[k] = User.get_user(v)
            else:
                kwargs_fixed[k] = v

class Entity(owned):
    pass

class Manapool(Entity):
    __slots__ = ('owner', 'managen', 'mana')

    def __init__(self, owner=None, managen=1.0, **kwargs):
        self.owner = owner
        self.managen = managen
        self.mana = 0.0
