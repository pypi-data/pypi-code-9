# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _
from django.db import models

from . import load_class
from .settings import WRITEBACK_BASE_MODEL


class MessageAbstract(models.Model):
    """
    Abstract base class, representing a feedback message.
    """
    date_created = models.DateTimeField(_('registration date and time'), max_length=20, auto_now_add=True)
    name = models.CharField(_('name'), max_length=20, blank=True, null=True)
    middle_name = models.CharField(_('middle name'), max_length=20, blank=True, null=True)
    family_name = models.CharField(_('family name'), max_length=50, blank=True, null=True)
    company = models.CharField(_('company'), max_length=50, blank=True, null=True)
    phone = models.CharField(_('phones'), max_length=250, blank=True, null=True)
    email = models.EmailField(_('email'), max_length=50, blank=True, null=True)
    info = models.TextField(_('info'), blank=True, null=True)

    class Meta:
        verbose_name = _('message')
        verbose_name_plural = _('messages')
        abstract = True

    def __unicode__(self):
        return u'%s %s %s %s %s %s' % (self.name, self.middle_name, self.family_name, self.company, self.phone,
                                       self.email)


class Message(load_class(WRITEBACK_BASE_MODEL)):
    """
    Class, representing a feedback message.
    """
    pass
