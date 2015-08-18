from django.db import models
from django.utils.translation import ugettext_lazy as _

from model_utils.managers import InheritanceManager
from djmoney.models.fields import MoneyField


class BaseTransaction(models.Model):
    PENDING = 1
    DONE = 2
    VERIFIED = 3
    INVALID = 4
    STATUS_CHOICES = (
        (PENDING, _('Pending')),
        (DONE, _('Done')),
        (VERIFIED, _('Verified')),
        (INVALID, _('Rejected/Canceled/Others')),
    )

    amount = MoneyField(_('amount'), max_digits=12, decimal_places=2, default_currency='USD', blank=True, null=True)
    creation_dt = models.DateTimeField(_('creation date'), auto_now_add=True)
    start_dt = models.DateTimeField(_('start date'), blank=True, null=True)
    end_dt = models.DateTimeField(_('end date'), blank=True, null=True)
    status = models.PositiveSmallIntegerField(_('status'), choices=STATUS_CHOICES, default=PENDING)

    objects = InheritanceManager()
