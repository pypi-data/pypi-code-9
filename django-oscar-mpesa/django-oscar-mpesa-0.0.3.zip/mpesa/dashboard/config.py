from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class MpesaDashboardConfig(AppConfig):
    label = 'mpesa_dashboard'
    name = 'mpesa.dashboard'
    verbose_name = _('MPesa')
