import requests
from django.core.validators import ValidationError
from django.conf import settings
from django.utils.translation import gettext_lazy as _


def validate_email_mailgun(value):
    try:
        public_key = getattr(settings, 'MAILGUN_PUBLIC_KEY')
        r = requests.get(
                "https://api.mailgun.net/v3/address/validate",
                auth=("api", public_key),
                params={"address": value})
        if r.status_code == 200:
            response = r.json()
            if response['is_valid'] is not True:
                if response['did_you_mean'] is not None:
                    raise ValidationError(_('Did you mean %(did_you_mean)s?') % response)
                else:
                    raise ValidationError('Email is invalid')
    except (AttributeError, requests.ConnectionError):
        pass
    return True
