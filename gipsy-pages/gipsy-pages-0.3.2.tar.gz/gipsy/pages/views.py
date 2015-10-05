#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = u"Rafał Selewońko <rafal@selewonko.com>"


from gipsy.pages.models import Page
from gipsy.pages.views_base import PageDetailView as PageDetailViewBase


class PageDetailView(PageDetailViewBase):
    model = Page
    queryset = Page.objects.active()

page_detail = PageDetailView.as_view()
