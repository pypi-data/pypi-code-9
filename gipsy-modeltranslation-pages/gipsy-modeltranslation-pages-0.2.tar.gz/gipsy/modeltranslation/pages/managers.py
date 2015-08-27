#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = u"Rafał Selewońko <rafal@selewonko.com>"

from modeltranslation.manager import MultilingualManager
from modeltranslation.manager import MultilingualQuerySet

from gipsy.pages.managers import PageManager as PageManagerBase
from gipsy.pages.managers import PageQuerySet as PageQuerySetBase


class PageQuerySet(PageQuerySetBase, MultilingualQuerySet):
    pass


class PageManager(PageManagerBase, MultilingualManager):

    def get_queryset(self):
        return PageQuerySet(model=self.model, using=self._db)
