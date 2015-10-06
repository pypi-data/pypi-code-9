#!/usr/bin/python
#
# This file is part of PlainForm
# Copyright © 2015 Guillaume Ayoub
#
# BSD-Licensed


"""
PlainForm
=========

Formidable forms formed with WTForms.

"""

from wtforms.form import Form
from wtforms.fields import (
    Field, BooleanField, FileField, RadioField, SelectField,
    SelectMultipleField, SubmitField, StringField, HiddenField,
    PasswordField, TextAreaField)
from wtforms.fields.html5 import (
    SearchField, TelField, URLField, EmailField, DateField, DateTimeField,
    DateTimeLocalField, IntegerField, DecimalField, IntegerRangeField,
    DecimalRangeField)
from wtforms.widgets.core import html_params, HTMLString


VERSION = '0.1'


class Form(Form):
    def __init__(self, formdata=None, obj=None, prefix='', data=None,
                 meta=None, **kwargs):
        self.kwargs = kwargs
        if 'method' not in self.kwargs:
            self.kwargs['method'] = 'POST'
        super().__init__(formdata, obj, prefix, meta)
        
    def __call__(self):
        if 'enctype' not in self.kwargs:
            for field in self:
                if isinstance(field, FileField):
                    self.kwargs['enctype'] = 'multipart/form-data'
                    break
        return HTMLString('<form {}>\n{}\n</form>'.format(
            html_params(**self.kwargs), '\n'.join(field() for field in self)))


class Field(Field):
    def __init__(self, label=None, validators=None, filters=(), description='',
                 id=None, default=None, widget=None, _form=None, _name=None,
                 _prefix='', _translations=None, _meta=None, **kwargs):
        self.kwargs = kwargs
        super().__init__(
            label, validators, filters, description, id, default, widget,
            _form, _name, _prefix, _translations, _meta)

    def __call__(self, **kwargs):
        kwargs.update(self.kwargs)
        for flag in dir(self.flags):
            if not flag.startswith('_'):
                kwargs[flag] = getattr(self.flags, flag)
        return HTMLString(
            '{}\n{}'.format(self.label, self.widget(self, **kwargs)))


class BooleanField(BooleanField, Field):
    def __call__(self, **kwargs):
        kwargs.update(self.kwargs)
        return HTMLString(
            '{}\n{}'.format(self.widget(self, **kwargs), self.label))


class FileField(FileField, Field):
    pass


class RadioField(RadioField, Field):
    def __call__(self, **kwargs):
        kwargs.update(self.kwargs)
        return HTMLString('<p>{}</p>'.format(self.label.text) + '\n'.join(
            '{}\n{}'.format(field.widget(field, **kwargs), field.label)
            for field in self))


class SelectField(SelectField, Field):
    def __call__(self, **kwargs):
        kwargs.update(self.kwargs)
        return HTMLString(
            '{}\n{}'.format(self.label, self.widget(self, **kwargs)))


class SelectMultipleField(SelectMultipleField, SelectField):
    pass


class SubmitField(SubmitField, Field):
    def __call__(self, **kwargs):
        kwargs.update(self.kwargs)
        return self.widget(self, **kwargs)


class StringField(StringField, Field):
    pass


class HiddenField(HiddenField, Field):
    def __call__(self, **kwargs):
        kwargs.update(self.kwargs)
        return self.widget(self, **kwargs)


class PasswordField(PasswordField, Field):
    pass


class TextAreaField(TextAreaField, Field):
    pass


class SearchField(SearchField, Field):
    pass


class TelField(TelField, Field):
    pass


class URLField(URLField, Field):
    pass


class EmailField(EmailField, Field):
    pass


class DateField(DateField, Field):
    pass


class DateTimeField(DateTimeField, Field):
    pass


class DateTimeLocalField(DateTimeLocalField, Field):
    pass


class IntegerField(IntegerField, Field):
    pass


class DecimalField(DecimalField, Field):
    pass


class IntegerRangeField(IntegerRangeField, Field):
    pass


class DecimalRangeField(DecimalRangeField, Field):
    pass
