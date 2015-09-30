# -#- coding: utf-8 -#-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from feincms.translations import (TranslatedObjectManager,
                                  TranslatedObjectMixin, Translation)
from leonardo.module.media.models import Image


class LinkCategory(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("name"))
    slug = models.CharField(max_length=255, verbose_name=_("slug"), blank=True)
    description = models.TextField(blank=True, verbose_name=_("description"))

    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        verbose_name = _('Link list')
        verbose_name_plural = _('Link lists')


TARGET_CHOICES = (
    ('_none', _('Same window')),
    ('_blank', _('New window')),
    ('_modal', _('Modal window')),
)


class Link(models.Model, TranslatedObjectMixin):
    web_address = models.CharField(
        max_length=255, verbose_name=_("Link"))
    target = models.CharField(max_length=255, verbose_name=_(
        "target"), choices=TARGET_CHOICES, default='_none')
    relationship = models.ForeignKey('self',
                                     blank=True, null=True, verbose_name=_("link relationship"))
    image = models.ForeignKey(
        Image, blank=True, null=True, verbose_name=_("Image"))
    category = models.ForeignKey(LinkCategory, verbose_name=_("List"))
    visible = models.BooleanField(verbose_name=_("visible"), default=True)
    ordering = models.PositiveIntegerField(
        verbose_name=_("Ordering"), default=0)

    objects = TranslatedObjectManager()

    def __unicode__(self):
        trans = None

        # This might be provided using a .extra() clause to avoid hundreds of
        # extra queries:
        if hasattr(self, "preferred_translation"):
            trans = getattr(self, "preferred_translation", u"")
        else:
            try:
                trans = unicode(self.translation)
            except models.ObjectDoesNotExist:
                pass
            except AttributeError:
                pass

        if trans:
            return trans
        else:
            return self.web_address

    class Meta:
        ordering = ['ordering', ]
        verbose_name = _('Link item')
        verbose_name_plural = _('Link items')


class LinkTranslation(Translation(Link)):

    """
    Translated link name and description.
    """

    name = models.CharField(_('name'), max_length=200)
    description = models.TextField(_('description'), blank=True)

    class Meta:
        verbose_name = _('Translation')
        verbose_name_plural = _('Translations')

    def __unicode__(self):
        return self.name
