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
