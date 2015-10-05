#!/usr/bin/env python
# -*- coding: utf-8 -*-

u"""
This module does that.
"""
__author__ = u"Rafał Selewońko <rafal@selewonko.com>"


from optionsfield.fields import OptionsWidget
from gipsy.sections.forms_base import SectionAdminFormBase
from gipsy.modeltranslation.sections.models import Section
from django.conf import settings


class SectionAdminForm(SectionAdminFormBase):

    class Meta:
        model = Section
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(SectionAdminForm, self).__init__(*args, **kwargs)
        for language_code, _ in settings.LANGUAGES:
            try:
                self.fields['options_%s' % language_code].widget = OptionsWidget()
            except KeyError:
                pass

            try:
                self.fields['title_%s' % language_code].help_text = "Name of a object - used in " \
                    "templates as a <strong>headline</strong> or just for identification"
            except KeyError:
                pass

            try:
                self.fields['description_%s' % language_code].help_text = "<strong>copy,</strong> content of object"
            except KeyError:
                pass

            if 'tinymce' in settings.INSTALLED_APPS:
                from tinymce.widgets import TinyMCE
                try:
                    self.fields['description_%s' % language_code].widget = \
                        TinyMCE(attrs={'cols': 80, 'rows': 30})
                except KeyError:
                    pass


class SectionInlineAdminForm(SectionAdminForm):

    def __init__(self, *args, **kwargs):
        super(SectionInlineAdminForm, self).__init__(*args, **kwargs)
        self.fields['template_name'].help_text = None
        for language_code, _ in settings.LANGUAGES:
            # remove help text from inline formset as its too long and breaks look
            try:
                self.fields['title_%s' % language_code].help_text = None
            except KeyError:
                pass
