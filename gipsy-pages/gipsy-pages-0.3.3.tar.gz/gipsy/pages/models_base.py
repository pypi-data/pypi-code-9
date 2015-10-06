#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = u"Rafał Selewońko <rafal@selewonko.com>"

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import (ActivatorModel, TimeStampedModel,
                                         TitleDescriptionModel)

from filebrowser.fields import FileBrowseField
from mptt.models import MPTTModel, TreeForeignKey
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


class PageBase(MPTTModel, UserStampedModel, ActivatorModel,
               TitleDescriptionModel, TimeStampedModel):

    image = FileBrowseField(
        blank=True,
        directory="partners/images/",
        extensions=('.jpg', '.png', '.jpeg', '.gif'),
        max_length=255,
        null=True,
        verbose_name="Image")

    template_name = models.CharField(
        blank=True,
        null=True,
        max_length=255,
        verbose_name=_(u"template"))

    OPTIONS_TYPES = (
        unicode, str,
    )

    options = OptionsField(types=OPTIONS_TYPES, verbose_name=_(u"options"))

    # object embedded in page
    content_type = models.ForeignKey(ContentType, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    parent = TreeForeignKey(
        blank=True,
        db_index=True,
        null=True,
        related_name='children',
        to='self')

    slug = models.SlugField(verbose_name=_(u"slug"), blank=True)

    TEMPLATE_NAME_CHOICES = settings.GIPSY_PAGES_PAGE_TEMPLATE_NAME_CHOICES

    author = models.ForeignKey(
        to='auth.User',
        blank=True,
        null=True,
        verbose_name=_("author"),
        help_text=_("Name that is being displayed in frontend. Does not have "
                    "to be actual creator of this object"))

    class MPTTMeta:
        order_insertion_by = ['title']

    class Meta:
        verbose_name = _(u"page")
        verbose_name_plural = _(u"pages")
        unique_together = (('parent', 'slug'))
        abstract = True

    @property
    def path(self):
        pages = self.get_ancestors(ascending=False, include_self=True)
        path_elements = [page.slug for page in pages]
        return '/'.join(filter(bool, path_elements))

    def get_absolute_url(self):
        url = "/" + self.path
        if settings.APPEND_SLASH:
            url += '/'
        return url

    def __unicode__(self):
        return self.title
