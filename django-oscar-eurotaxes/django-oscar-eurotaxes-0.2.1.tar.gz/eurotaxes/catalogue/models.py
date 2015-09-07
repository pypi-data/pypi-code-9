# coding=utf-8
__copyright__ = 'Copyright 2015, Abalt'

from django.db import models
from django.utils.translation import ugettext_lazy as _

from oscar.apps.catalogue.abstract_models import AbstractProduct

from eurotaxes.partner.models import VATType


class Product(AbstractProduct):
    vat_type = models.ForeignKey(VATType, verbose_name=_('VAT Type'))


from oscar.apps.catalogue.models import *