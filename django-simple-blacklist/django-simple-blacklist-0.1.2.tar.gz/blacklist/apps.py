# coding=utf-8
# django-simple-blacklist 6/29/15 9:19 AM by mnach #
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class BlacklistConfig(AppConfig):
    name = 'blacklist'
    verbose_name = _("Blacklist")