#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = u"Rafał Selewońko <rafal@selewonko.com>"

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import (ActivatorModel, TimeStampedModel,
                                         TitleSlugDescriptionModel)
# from gipsy.menus.managers import MenuNodeManager
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


MENU_CONTENT_TYPES = (
    'pages.Page',
    'partners.Partner',
)


def get_menu_node_content_type_limit_choices_to():
    limit_choices_to = None
    for i in MENU_CONTENT_TYPES:
        app_label, model = i.split('.')
        q = models.Q(app_label__iexact=app_label, model__iexact=model)
        if limit_choices_to is None:
            limit_choices_to = q
        else:
            limit_choices_to |= q
    return limit_choices_to


class MenuNodeAbstract(MPTTModel, UserStampedModel, ActivatorModel,
                       TitleSlugDescriptionModel, TimeStampedModel):

    parent = TreeForeignKey(
        blank=True,
        db_index=True,
        null=True,
        related_name='children',
        to='self')

    STUB_MAIN = 'main'
    STUB_HEADER = 'header'
    STUB_FOOTER = 'footer'
    STUB_ASIDE = 'aside'
    STUB_CHOICES = (
        (None, _("No stub")),
        (STUB_MAIN, _("Main")),
        (STUB_HEADER, _("Header")),
        (STUB_FOOTER, _("Footer")),
        (STUB_ASIDE, _("Aside")),
    )

    stub = models.SlugField(
        choices=STUB_CHOICES,
        verbose_name=_(u"stub"),
        default=None,
        unique=True,
        blank=True,
        null=True)

    url = models.CharField(max_length=512, verbose_name=_(u"url"), blank=True)

    content_type = models.ForeignKey(ContentType, null=True, blank=True,
                                     limit_choices_to=get_menu_node_content_type_limit_choices_to)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    options = OptionsField(types=(unicode, str), verbose_name=_(u"options"))

    class Meta:
        abstract = True
        verbose_name = _(u"menu node")
        verbose_name_plural = _(u"menu nodes")
        get_latest_by = 'created'

    class MPTTMeta:
        order_insertion_by = ['created']

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):

        if self.content_object:
            return self.content_object.get_absolute_url()

        return self.url
