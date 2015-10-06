#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = u"Rafał Selewońko <rafal@selewonko.com>"


from django_extensions.db.models import (ActivatorModelManager,
                                         ActivatorQuerySet)
from mptt.managers import TreeManager


class PageQuerySet(ActivatorQuerySet):

    def get_by_path(self, path, slug_field='slug'):
        path_elements = filter(bool, (p for p in path.split('/')))

        # must be home page
        if not path_elements:
            path_elements = ['']

        f = {}
        for (i, slug) in enumerate(path_elements):
            l = '__'.join(['parent'] * (len(path_elements) - 1 - i))

            def a(b):
                return '__'.join([l, b]) if l else b

            f.update({a(slug_field): slug, a('level'): i})

        return self.get(**f)


class PageManager(ActivatorModelManager, TreeManager):

    def get_queryset(self):
        return PageQuerySet(model=self.model, using=self._db)

    def get_by_path(self, path):
        return self.get_queryset().get_by_path(path)
