#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = u"Rafał Selewońko <rafal@selewonko.com>"

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import six
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import (ActivatorModel, TimeStampedModel,
                                         TitleSlugDescriptionModel)
from filebrowser.fields import FileBrowseField

from optionsfield import OptionsField


class UserStampedModel(models.Model):

    created_by = models.CharField(
        blank=True,
        editable=False,
        max_length=128,
        null=True,
        verbose_name=_('Created by'))

    modified_by = models.CharField(
        blank=True,
        editable=False,
        max_length=128,
        null=True,
        verbose_name=_('Modified by'))

    class Meta:
        abstract = True

    def save(self, by=None, *args, **kwargs):
        if by:
            if self.pk is None:
                self.created_by = by
            else:
                self.modified_by = by

        super(UserStampedModel, self).save(*args, **kwargs)


class SectionBase(UserStampedModel, ActivatorModel, TitleSlugDescriptionModel,
                  TimeStampedModel):

    order = models.PositiveIntegerField(
        default=0,
        verbose_name=_(u"order"))

    image = FileBrowseField(
        blank=True,
        directory="partners/images/",
        extensions=('.jpg', '.png', '.jpeg', '.gif'),
        max_length=255,
        null=True,
        verbose_name="Image")

    TEMPLATE_NAME_CHOICES = getattr(
        settings, 'GIPSY_SECTIONS_SECTION_TEMPLATE_NAME_CHOICES')

    template_name = models.CharField(
        blank=True,
        null=True,
        max_length=255,
        verbose_name=_(u"template"),
        help_text=_("Defines template type in which this object will be "
                    "rendered. Various templates have different look and "
                    "use different fields and options. Please refer to "
                    "documentation for details on template types."))

    OPTIONS_TYPES = six.string_types

    options = OptionsField(types=OPTIONS_TYPES, verbose_name=_(u"options"))

    # parent section or other object to which this section is connect to
    section_content_type = models.ForeignKey(
        to=ContentType, related_name='sections',
        null=True, blank=True, help_text=_(
            "Specifies type of object to which this section is attached to. Do not "
            "change if you're unsure what does that it do."))
    section_object_id = models.PositiveIntegerField(
        null=True, blank=True, help_text=_(
            "Specifies object to which this section is attached to. Do not "
            "change if you're unsure what does that it do."))
    section_content_object = GenericForeignKey('section_content_type', 'section_object_id')

    # object embedded in section
    content_type = models.ForeignKey(ContentType, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        abstract = True
        verbose_name = _(u"section")
        verbose_name_plural = _(u"sections")
        ordering = ('order',)
        get_latest_by = 'created'

    def __unicode__(self):
        return self.title

    def get_description(self):
        if self.description:
            description = self.description
        elif self.content_object and self.content_object.description:
            description = self.content_object.description
        else:
            description = None
        return description
