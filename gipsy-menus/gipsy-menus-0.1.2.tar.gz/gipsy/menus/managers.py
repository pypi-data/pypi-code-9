#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = u"Rafał Selewońko <rafal@selewonko.com>"


from django_extensions.db.models import (ActivatorModelManager,
                                         ActivatorQuerySet)
from mptt.managers import TreeManager


class MenuNodeQuerySet(ActivatorQuerySet):
    pass


class MenuNodeManager(ActivatorModelManager, TreeManager):

    def get_queryset(self):
        return MenuNodeQuerySet(model=self.model, using=self._db)
