#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = u"Rafał Selewońko <rafal@selewonko.com>"

from django.contrib.contenttypes.models import ContentType
from modeltranslation.manager import MultilingualManager
from modeltranslation.manager import MultilingualQuerySet

from gipsy.sections.managers import SectionManager as SectionManagerBase
from gipsy.sections.managers import SectionQuerySet as SectionQuerySetBase


class SectionQuerySet(SectionQuerySetBase, MultilingualQuerySet):
    pass


class SectionManager(SectionManagerBase, MultilingualManager):

    def get_queryset(self):
        return SectionQuerySet(model=self.model, using=self._db)


def SectionsManager():
    "Related sections manager"
    # FIXME: make that not related to modeltranslation version
    @property
    def wrap(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        from gipsy.modeltranslation.sections.models import Section
        return Section.objects.filter(
            section_content_type=content_type,
            section_object_id=self.id)
    return wrap
