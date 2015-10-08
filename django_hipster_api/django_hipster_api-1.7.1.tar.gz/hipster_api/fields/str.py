# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from hipster_api.fields.base import Field
import json


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
        try:
            value = value.replace(' ', '').split(self.separator)
        except UnicodeDecodeError:
            value = value.replace(str(' '), str('')).split(str(self.separator))

        value = value if all(value) else list()
        self.value = value
        return self.value


class FieldsListResponse(StringList):

    global_fields = ['password', 'pwd']

    def __exclude_global_fields(self, request, sep):
        self.setitem(list(filter(
            lambda field: len(list(
                set(self.global_fields) & set(field.split(sep))
            )) == 0, self.value
        )))

    def exclude_global_fields(self, request):
        sep = '__'
        try:
            self.__exclude_global_fields(request, sep)
        except UnicodeDecodeError:
            sep = str(sep)
            self.global_fields = list(map(str, self.global_fields))
            self.__exclude_global_fields(request, sep)

    rules = (
        exclude_global_fields,
    )


class JsonField(String):
    def to_python(self):
        value = super(JsonField, self).to_python()
        try:
            self.setitem(json.loads(value))
        except ValueError:
            self.setitem(self.default)

        return self.value
