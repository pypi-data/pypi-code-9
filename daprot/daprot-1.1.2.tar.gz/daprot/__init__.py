
# -*- coding: utf-8 -*-

"""
daprot is a data flow prototyper and mapper library.
Copyright (C) 2015, Bence Faludi (bence@ozmo.hu)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, <see http://www.gnu.org/licenses/>.
"""

import copy
from bisect import bisect
from . import mapper, exceptions as exc
from types import FunctionType
from collections import Iterable, Callable
from funcomp import Composition
from dm import Mapper

class Field(object):
    _creation_counter = 0

    # void
    def __init__(self, route = None, type = None, default_value = None, \
                 transforms = None, name = None ):
        self.name = name
        self.type = type
        self.route = route
        self.default_value = default_value
        self.index = None
        self.transforms = transforms

        self._creation_counter = Field._creation_counter
        Field._creation_counter += 1

    # tuple
    def transforms():
        def fget(self):
            return self._transforms

        def fset(self, transforms):
            if not transforms:
                transforms = []

            if not isinstance(transforms, Iterable):
                transforms = [transforms]

            self._transforms = Composition(*iter(transforms))

        def fdel(self):
            self._transforms = []

        return locals()

    transforms = property(**transforms())

    # int
    def __cmp__(self, other):
        return cmp( self._creation_counter, other._creation_counter )

    # bool
    def __lt__(self, other):
        return self._creation_counter < other._creation_counter

    # str
    def retriev_route(self, default_mapper):
        if type(self.route) is FunctionType:
            return self.route(self)

        if self.route is not None:
            return self.route

        return default_mapper(self)

    # type
    def retriev_default_value(self):
        if self.default_value is None:
            return None

        if isinstance(self.default_value, Callable):
            return self.default_value()

        return self.default_value

    # type
    def convert_value(self, value):
        if self.type is None:
            return value

        return self.type(value)

    # type
    def retriev_value(self, value):
        cv = self.convert_value(value)
        if cv is None:
            return self.retriev_default_value()

        return self.transforms(cv)

class NestedField(object):
    # str
    def retriev_route(self, default_mapper):
        return super(NestedField, self).retriev_route(default_mapper \
            if self.route is not None else mapper.INHERITED)

class ListOf(NestedField, Field):
    # void
    def __init__(self, prototype, route, default_value = None, \
                 transforms = None, name = None):
        self.prototype = prototype
        super(ListOf, self).__init__(route, None, default_value or [], transforms, name)

    # list
    def retriev_value(self, value):
        if value is None: return self.retriev_default_value()
        cv = list(self.prototype(value, mapper=self.parent.mapper))
        return self.transforms(cv)

class DictOf(NestedField, Field):
    # void
    def __init__(self, prototype, route = None, default_value = None, \
                 transforms = None, name = None):
        self.prototype = prototype
        super(DictOf, self).__init__(route, None, default_value or {}, transforms, name)

    # dict
    def retriev_value(self, value):
        if value is None: return self.retriev_default_value()
        schema_flow = self.prototype([value], mapper=self.parent.mapper)
        return self.transforms(DataFrame(schema_flow, value))

class Prototype(object):
    # void
    def __init__(self, *fields):
        if not len(fields):
            raise exc.FieldRequired('Prototype requires at least one Field!')

        known_field_names = set()
        for field in fields:
            if not field.name:
                raise exc.FieldNameRequired("Field's name attribute is required!")

            if field.name in known_field_names:
                raise exc.FieldNameNotUnique("Field's name must be unique!")

            known_field_names.add(field.name)

        self.fields = fields
        self.reindex()

    # void
    def reindex(self):
        for index in range(len(self.fields)):
            self.fields[index].index = index

    # dict
    def retriev_routes(self, default_mapper):
        return { field.name : field.retriev_route(default_mapper) \
            for field in self.fields }

class PrototypeGenerator(type):
    def __new__(metacls, name, bases, namespace, **kwds):
        cls, fields = super(PrototypeGenerator, metacls) \
            .__new__(metacls, name, bases, dict(namespace)), []
        for name, obj in namespace.items():
            if isinstance(obj, Field):
                obj.name = name
                fields.insert(bisect(fields, obj), obj)

        if len(fields):
            cls.prototype = Prototype(*fields)

        return cls

class DataFrame(dict):
    def __new__(cls, df, data):
        return { name : getattr(df, name).retriev_value(value) for name, value \
            in Mapper(data, routes = df.routes).getRoutes().items() }

# Python 2 & 3 metaclass decorator from `six` package.
def add_metaclass(metaclass):
    def wrapper(cls):
        orig_vars = cls.__dict__.copy()
        slots = orig_vars.get('__slots__')
        if slots is not None:
            if isinstance(slots, str):
                slots = [slots]
            for slots_var in slots:
                orig_vars.pop(slots_var)
        orig_vars.pop('__dict__', None)
        orig_vars.pop('__weakref__', None)
        return metaclass(cls.__name__, cls.__bases__, orig_vars)
    return wrapper

@add_metaclass(PrototypeGenerator)
class SchemaFlow(object):
    # void
    def __init__(self, iterable, mapper = mapper.IGNORE, prototype = None, \
                 offset = 0, limit = None):
        if not hasattr(self, 'prototype'):
            if not prototype:
                raise exc.PrototypeRequired( \
                    'Prototype declaration is required for DataFlow!')

            self.prototype = prototype

        elif prototype:
            raise exc.PrototypeAlreadySet( \
                'DataFlow object has already a Prototype!')

        for field in self.prototype.fields:
            setattr(self, field.name, copy.copy(field))
            if isinstance(field, NestedField):
                getattr(self, field.name).parent = self

        self.routes = self.prototype.retriev_routes(mapper)
        self.mapper = mapper
        self.offset = offset
        self.limit = limit
        self.index = 0
        self.iterable = iter(iterable)

    # list<>
    def get_fields(self):
        return [ getattr(self, field.name) for field in self.prototype.fields ]

    # bool
    def is_nested(self):
        for field in self.get_fields():
            if isinstance(field, NestedField):
                return True

        return False

    # SchemaFlow
    def __iter__(self):
        return self

    # dict
    def next(self):
        if not self.iterable or ( self.limit and self.index >= self.offset+self.limit ):
            raise StopIteration

        if self.index < self.offset:
            for p in range(self.offset): next(self.iterable)
            self.index = self.offset

        self.index += 1
        return DataFrame(self, next(self.iterable))

    # dict
    __next__ = next
