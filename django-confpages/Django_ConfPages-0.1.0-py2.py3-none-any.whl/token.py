from __future__ import absolute_import

import uuid

from django.core import signing

from .conf import settings


def make_token():
    """Generate a cryptographically signed token."""
    data = uuid.uuid4().hex
    token = signing.dumps(data)
    return token


def check_token(token):
    """Check whether the one-time token is valid."""
    if token is None:
        return False, 'Missing one-time token'

    try:
        signing.loads(token, max_age=settings.TOKEN_EXPIRES)
        return True, ''
    except signing.SignatureExpired:
        return False, 'Expired one-time token'
    except signing.BadSignature:
        return False, 'Invalid one-time token'
