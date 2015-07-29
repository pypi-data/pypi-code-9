#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = u"Rafał Selewońko <rafal@selewonko.com>"


from gipsy.pages.models import Page
from gipsy.pages.forms_base import PageAdminFormBase


class PageAdminForm(PageAdminFormBase):

    class Meta:
        model = Page
        fields = '__all__'
