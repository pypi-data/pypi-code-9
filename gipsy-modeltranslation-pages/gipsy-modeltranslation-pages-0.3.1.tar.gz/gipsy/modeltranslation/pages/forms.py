#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = u"Rafał Selewońko <rafal@selewonko.com>"


from gipsy.modeltranslation.pages.models import Page
from gipsy.pages.forms_base import PageAdminFormBase

from optionsfield.fields import OptionsWidget
from django.conf import settings


class PageAdminForm(PageAdminFormBase):

    class Meta:
        model = Page
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(PageAdminForm, self).__init__(*args, **kwargs)
        for language_code, _ in settings.LANGUAGES:
            try:
                self.fields['options_%s' % language_code].widget = OptionsWidget()
            except KeyError:
                pass

            try:
                self.fields['title_%s' % language_code].help_text = "Title of a object - used in " \
                    "templates as a <strong>headline</strong> and in meta title."
            except KeyError:
                pass

            try:
                self.fields['description_%s' % language_code].help_text = "Used in some templates as " \
                    "<strong>lead copy</strong> and in meta description."
            except KeyError:
                pass

            if 'tinymce' in settings.INSTALLED_APPS:
                from tinymce.widgets import TinyMCE
                try:
                    self.fields['description_%s' % language_code].widget = \
                        TinyMCE(attrs={'cols': 80, 'rows': 30})
                except KeyError:
                    pass
