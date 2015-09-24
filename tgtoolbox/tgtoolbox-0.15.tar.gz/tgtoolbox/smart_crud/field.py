# -*- coding: utf-8 -*-
__author__ = 'vahid'

class Field(object):
    def __init__(self, sa_column, **kw):
        self.sa_column = sa_column
        for k, v in kw.items():
            setattr(self, k, v)

    @property
    def name(self):
        return self.sa_column.name

    @property
    def label(self):
        if hasattr(self, 'alias'):
            return self.alias
        return self.name

    @property
    def display_label(self):
        title = self.label.replace('_', ' ')
        return title[:1].upper() + title[1:]

    @property
    def type(self):
        return self.sa_column.type
