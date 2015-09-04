# -*- coding: utf-8 -*-
from __future__ import unicode_literals


class Field(object):

    def __init__(
            self,
            verbose_name=None,
            default=None,
            rules=None,
            methods=None
    ):
        self.__rules = (rules or tuple()) + getattr(self.__class__, 'rules', tuple())
        self.default = default
        self.value = default
        self.methods = methods or ['get', 'put', 'post', 'delete']
        self.verbose_name = verbose_name or self.__class__.__name__

    def to_python(self):
        return self.value

    def to_rules(self, request):
        tuple(map(lambda fn: fn(self, request), self.__rules))
        return self

    def setitem(self, value):
        self.value = value
        return self
