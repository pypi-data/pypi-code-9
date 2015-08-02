#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = u"Rafał Selewońko <rafal@selewonko.com>"


import re

from django.core.exceptions import ValidationError
from django.db import models
from django.forms import fields
from django.utils import six
from django.utils.text import slugify

from .options import Options
from .widgets import OptionsWidget


class OptionsFormField(fields.CharField):
    widget = OptionsWidget

    def __init__(self, *args, **kwargs):
        kwargs['required'] = False
        return super(OptionsFormField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if isinstance(value, Options):
            return value

        if value:
            return Options.from_string(value)

    def clean(self, options):
        for key, value in options.items():
            if not re.match(r'^[a-zA_Z]+\w*$', key):
                key_ok = slugify(key).replace('-', '_').lstrip('_1234567890')
                msg = "Invalid option key: '{}'. You can use '{}'."
                raise ValidationError(msg.format(key, key_ok))
        return options


class OptionsField(six.with_metaclass(models.SubfieldBase, models.TextField)):

    def __init__(self, types=None, *args, **kwargs):

        self.types = types

        kwargs['blank'] = True
        kwargs['default'] = Options(types=self.types)

        return super(OptionsField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'form_class': OptionsFormField,
                    'widget': OptionsWidget}
        defaults.update(kwargs)
        return super(OptionsField, self).formfield(**defaults)

    def deconstruct(self):
        name, path, args, kwargs = super(OptionsField, self).deconstruct()

        del kwargs['blank']
        del kwargs['default']

        if self.types is not None:
            kwargs["types"] = self.types

        return name, path, args, kwargs

    def _parse_options(self, value):
        """
        Takes a string value of options and converts into a Options object
        """

        if isinstance(value, bytes):
            value = value.decode('utf8')

        try:
            value = Options.from_string(value, types=self.types)
        except ValueError:
            raise ValidationError("Invalid input for a Options instance")

        return value

    def from_db_value(self, value, *args, **kwargs):
        if value is None:
            return Options(types=self.types)
        return self._parse_options(value)

    def to_python(self, value):
        if value is None:
            return Options(types=self.types)
        if isinstance(value, Options):
            return value
        return self._parse_options(value)

    def get_prep_value(self, value):
        if not isinstance(value, Options):
            raise ValidationError('Not an Options instance')
        return value.to_string()

    def get_prep_lookup(self, lookup_type, value):
        # We only handle 'exact' lookup. All others are errors.
        if lookup_type == 'exact':
            return self.get_prep_value(value)
        else:
            raise TypeError('Lookup type %r not supported.' % lookup_type)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_prep_value(value)
