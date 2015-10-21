# -*- coding: utf-8 -*-
from __future__ import unicode_literals


class CRUDMixin(object):

    @classmethod
    def create(cls, **kwargs):
        obj = cls()
        for k, v in kwargs.iteritems():
            setattr(obj, k, v)
        return obj


class Model(CRUDMixin, object):
    __abstract__ = True
