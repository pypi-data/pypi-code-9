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

    def __init__(self, larger, equals=False, **kwargs):
        self.larger = larger
        self.equals = equals
        super(IntegerLarger, self).__init__(**kwargs)

    def to_python(self):
        value = super(IntegerLarger, self).to_python()
        if self.equals:
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


class IntegerLess(Integer):
    def __init__(self, less, equals=False, **kwargs):
        self.less = less
        self.equals = equals
        super(IntegerLess, self).__init__(**kwargs)

    def to_python(self):
        value = super(IntegerLess, self).to_python()
        if self.equals:
            if value > self.less:
                value = self.default
        elif value >= self.less:
            value = self.default
        self.value = value
        return value


class Float(Field):
    def to_python(self):
        value = super(Float, self).to_python()
        try:
            value = float(str(value).replace(',', '.'))
        except ValueError:
            value = self.default
        self.setitem(value)
        return self.value


class FloatLess(Float):
    def __init__(self, less, equals=False, **kwargs):
        self.less = less
        self.equals = equals
        super(FloatLess, self).__init__(**kwargs)

    def to_python(self):
        value = super(FloatLess, self).to_python()
        if self.equals:
            if value > self.less:
                value = self.default
        elif value >= self.less:
            value = self.default
        self.value = value


class FloatLarger(Float):
    def __init__(self, larger, equals=False, **kwargs):
        self.larger = larger
        self.equals = equals
        super(FloatLarger, self).__init__(**kwargs)

    def to_python(self):
        value = super(FloatLarger, self).to_python()
        if self.equals:
            if value < self.larger:
                value = self.default
        elif value <= self.larger:
            value = self.default
        self.value = value


class FloatList(_StringList):
    def to_python(self):
        value = super(FloatList, self).to_python()
        try:
            if self.separator != ',':
                value = list(map(lambda x: float(x.replace(',', '.')), value))
            else:
                value = list(map(lambda x: float(x), value))
        except ValueError:
            self.value = self.default
            return self.to_python()
        self.value = value
