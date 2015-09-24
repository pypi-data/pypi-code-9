# -*- coding: utf-8 -*-
import tw2.core as twc
from sprox.widgets import \
    PasswordField as _PasswordField, \
    TextField as _TextField
__author__ = 'vahid'

__all__ = [
    'PasswordField',
    'TextField',
]

class PasswordField(_PasswordField):
    css_class = 'form-control'

class TextField(_TextField):
    css_class = 'form-control'


