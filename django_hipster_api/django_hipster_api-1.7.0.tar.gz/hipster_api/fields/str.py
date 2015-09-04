# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from hipster_api.fields.base import Field


class String(Field):
    def __init__(self, default='', **kwargs):
        kwargs['default'] = default
        super(String, self).__init__(**kwargs)

    def to_python(self):
        value = super(String, self).to_python()
        try:
            try:
                value = str(value)
            except UnicodeEncodeError:
                value = unicode(value)
        except ValueError:
            value = str(self.default)

        self.value = value
        return value


class StringList(String):

    def __init__(self, separator=',', **kwargs):
        self.separator = separator
        super(StringList, self).__init__(**kwargs)

    def to_python(self):
        value = super(StringList, self).to_python()
        value = value.replace(' ', '').split(self.separator)
        value = value if all(value) else list()
        self.value = value
        return self.value


class FieldsListResponse(StringList):

    global_fields = ['password', 'pwd']

    def exclude_global_fields(self, request):
        self.setitem(list(filter(
            lambda field: len(list(
                set(self.global_fields) & set(field.split('__'))
            )) == 0, self.value
        )))

    rules = (
        exclude_global_fields,
    )
