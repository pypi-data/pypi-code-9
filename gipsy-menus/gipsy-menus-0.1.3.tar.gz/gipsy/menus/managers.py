#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = u"Rafał Selewońko <rafal@selewonko.com>"


from django_extensions.db.models import (ActivatorModelManager,
                                         ActivatorQuerySet)
from mptt.managers import TreeManager, TreeQuerySet


class MenuNodeQuerySet(TreeQuerySet, ActivatorQuerySet):
    pass


class MenuNodeManager(TreeManager, ActivatorModelManager):
    pass
