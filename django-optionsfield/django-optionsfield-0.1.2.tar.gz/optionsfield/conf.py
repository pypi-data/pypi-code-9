#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = u"Rafał Selewońko <rafal@selewonko.com>"

from django.conf import settings as django_settings

from . import default_settings


class OptionsFieldSettings():
    prefix = "OPTIONSFIELD_"

    def __getattr__(self, name):
        try:
            return getattr(django_settings, "".join((self.prefix, name)))
        except AttributeError:
            return getattr(default_settings, name)

settings = OptionsFieldSettings()
