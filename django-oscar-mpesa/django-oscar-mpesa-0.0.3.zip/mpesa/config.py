from django.apps import AppConfig
from django.conf import settings
from django.core.checks import Error, register
from django.utils.translation import ugettext_lazy as _


REQUIRED_SETTINGS = ["MPESA_PAYBILL_NUMBER", "MPESA_IPN_USER", "MPESA_IPN_PASS"]


class MpesaConfig(AppConfig):
    label = 'mpesa'
    name = 'mpesa'
    verbose_name = _('MPesa Payment Method')

    def ready(self):
        # Register the signal handlers
        from .signals import handlers


@register
def missing_settings_check(app_configs, **kwargs):
    """
    Triggers a system check error if one of the required settings is missing.
    """
    errors = []
    for name in REQUIRED_SETTINGS:
        required_setting = getattr(settings, name, None)
        if not required_setting:
            errors.append(
                Error(
                    "Missing setting",
                    "Please set {} in your settings".format(name),
                    id="mpesa.E001",
                )
            )
    return errors


@register
def invalid_ipn_pass_check(app_configs, **kwargs):
    errors = []
    ipn_pass = getattr(settings, 'MPESA_IPN_PASS', None)
    if ipn_pass:
        if len(ipn_pass) > 20:
            errors.append(
                Error(
                    "Invalid value for MPESA_IPN_PASS",
                    "Your password needs to be 20 characters or less",
                    id="mpesa.E002",
                )
            )
    return errors
