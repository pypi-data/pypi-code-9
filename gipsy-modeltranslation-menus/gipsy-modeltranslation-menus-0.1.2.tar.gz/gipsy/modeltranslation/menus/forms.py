#!/usr/bin/env python
# -*- coding: utf-8 -*-

u"""
This module does that.
"""
__author__ = u"Rafał Selewońko <rafal@selewonko.com>"


from optionsfield.fields import OptionsWidget

from gipsy.modeltranslation.menus.models import MenuNode
from gipsy.menus.forms_base import MenuNodeAdminFormBase

from django.conf import settings


class MenuNodeAdminForm(MenuNodeAdminFormBase):

    class Meta:
        model = MenuNode
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(MenuNodeAdminForm, self).__init__(*args, **kwargs)
        for language_code, language_name in settings.LANGUAGES:
            try:
                self.fields['options_%s' % language_code].widget = OptionsWidget()
            except KeyError:
                pass

    def _validate_url_and_content_object(self):
        # required only for main language
        url_field = 'url_%s' % settings.LANGUAGE_CODE
        super(MenuNodeAdminForm, self)._validate_url_and_content_object(url_field)
