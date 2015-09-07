# coding=utf-8
__copyright__ = 'Copyright 2015, Abalt'

from django.db import models
from django.utils.translation import ugettext_lazy as _

from decimal import Decimal

from oscar.apps.address.models import Country
from oscar.apps.partner.models import *  # noqa

from eurotaxes.partner.managers import VATCountryManager


class VATType(models.Model):
    name = models.CharField(max_length=50, verbose_name=_('Name'))
    default = models.BooleanField(default=False, verbose_name=_('Default'))

    class Meta:
        verbose_name = _('VAT Type')
        verbose_name_plural = _('VAT Types')

    def __unicode__(self):
        return u'%s' % self.name


class VATCountry(models.Model):
    country = models.ForeignKey(Country, verbose_name=_('Country'))
    vat_type = models.ForeignKey(VATType, verbose_name=_('VAT Type'))
    default = models.BooleanField(default=False, verbose_name=_('Default'))
    vat = models.DecimalField(decimal_places=2, max_digits=4, verbose_name=_('VAT'))

    objects = VATCountryManager()

    @property
    def get_vat(self):
        return self.vat / Decimal(100)

    class Meta:
        verbose_name = _('VAT Country')
        verbose_name_plural = _('VAT Countries')

    def __unicode__(self):
        return u'%s - %s' % (self.country, self.vat)
