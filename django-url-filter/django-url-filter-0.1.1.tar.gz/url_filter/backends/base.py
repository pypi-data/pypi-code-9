# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
import abc

import six


class BaseFilterBackend(six.with_metaclass(abc.ABCMeta, object)):
    def __init__(self, queryset, context=None):
        self.queryset = queryset
        self.context = context or {}

    def bind(self, specs):
        self.specs = specs

    @abc.abstractmethod
    def filter(self):
        pass
