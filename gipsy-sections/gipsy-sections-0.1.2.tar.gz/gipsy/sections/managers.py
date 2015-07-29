#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = u"Rafał Selewońko <rafal@selewonko.com>"

from django.contrib.contenttypes.models import ContentType
from django_extensions.db.models import (ActivatorModelManager,
                                         ActivatorQuerySet)


class SectionQuerySet(ActivatorQuerySet):
    pass


class SectionManager(ActivatorModelManager):

    def get_queryset(self):
        return SectionQuerySet(model=self.model, using=self._db)


def SectionsManager():
    "Related sections manager"
    @property
    def wrap(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        from gipsy.sections.models import Section
        return Section.objects.filter(
            section_content_type=content_type,
            section_object_id=self.id)
    return wrap
