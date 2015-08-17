# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from hipster_api.fields.base import Field
from hipster_api.fields.str import StringList as _StringList


class Integer(Field):
    def to_python(self):
        value = super(Integer, self).to_python()

        try:
            value = int(value)
        except ValueError:
            value = self.default

        self.setitem(value)
        return value


class IntegerLarger(Integer):

    def __init__(self, larger, glt=False, **kwargs):
        self.larger = larger
        self.glt = glt
        super(IntegerLarger, self).__init__(**kwargs)

    def to_python(self):
        value = super(IntegerLarger, self).to_python()
        if self.glt:
            if value < self.larger:
                value = self.default
        elif value <= self.larger:
            value = self.default
        self.value = value
        return value


class IntegerList(_StringList):
    def to_python(self):
        value = super(IntegerList, self).to_python()
        try:
            value = list(map(lambda x: int(x), value))
        except ValueError:
            self.value = self.default
            return self.to_python()
        self.value = value
        return value
