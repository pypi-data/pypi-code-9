#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = u"Rafał Selewońko <rafal@selewonko.com>"

import collections

from . import codec
from .conf import settings


class Options(collections.MutableMapping):

    __options = None

    def __init__(self, types=None):
        self.__options = collections.OrderedDict()
        if types is None:
            types = settings.DEFAULT_TYPES
        self._types = types

    def __getitem__(self, key):
        return self.__options[key]

    def __setitem__(self, key, value):
        self._add_option(key, value)

    def __delitem__(self, key):
        del self.__options[key]

    def __iter__(self):
        return iter(self.__options)

    def __len__(self):
        return len(self.__options)

    def __keytransform__(self, key):
        return key

    def __getattr__(self, key):
        try:
            option = self.__options[key]
        except KeyError:
            raise AttributeError(key)
        else:
            return option

    def __setattr__(self, key, value):
        if not key.startswith('_'):
            self._add_option(key, value)
        else:
            super(Options, self).__setattr__(key, value)

    def _add_option(self, key, value):
        if type(value) not in self._types:
            raise ValueError("Type '%s' not allowed" % type(value).__name__)
        self.__options[key] = value

    def __str__(self):
        return "{}({})".format(self.__class__.__name__, self.to_string())

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, self.to_string())

    @classmethod
    def from_string(cls, string, types=None):
        instance = cls(types)
        options = codec.decode(string)
        if isinstance(options, dict):
            instance.__options = options
        return instance

    def to_string(self):
        return codec.encode(self.__options)

    def __eq__(self, obj):
        return self.__options.__eq__(obj)

    def __hash__(self):
        return self.to_string().__hash__
