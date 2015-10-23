# -*- coding: utf-8 -*-
from __future__ import absolute_import

import string
import six

from email_validation import valid_email_address

from .utils import deprecated


def _true_or_value_error(exp, msg="validation failed"):
    if not exp:
        raise ValueError(msg)
    return exp


def _is_valid_stringfield(arg, min_len=1, max_len=None):
    if not isinstance(arg, six.string_types):
        raise TypeError("field must be a string, received: %r" % arg)
    if len(arg) < min_len:
        raise ValueError("field must be at least %d chars long" % min_len)
    if (max_len is not None) and (len(arg) > max_len):
        raise ValueError("String is too long")
    return str(arg)


VALIDATORS = {
    'name': _is_valid_stringfield,
    # min length is not our business.
    'password': lambda x: _true_or_value_error(
        _is_valid_stringfield(x, max_len=64) and set(x).issubset(string.printable),
        "Passwords must be a subset of ASCII, max_len=64"
    ),
    'displayName': lambda x: _is_valid_stringfield(x, max_len=128),
    'Language': lambda x: _true_or_value_error(
        x in ("en", "de", "es", "fr", "it", "ja", "ko",
              "pt", "zh_CN", "fi", "pl", "zh_TW", "th", "ru"),
        "Unsupported language: %r" % x
    ),
    'groupName': _is_valid_stringfield,
    'proxyName': _is_valid_stringfield,
    # extensions can have leading zeros but must be numeric to int
    'extension': lambda x: _true_or_value_error(
        str(x).isdigit() and len(str(x)) < 17,
        "Extension (%s) is out of range" % x
    ),
    'emailAddress': lambda x: _true_or_value_error(
        valid_email_address(x),
        "email address '%r' is invalid" % x
    ),
    'RoleName': _is_valid_stringfield,
    'description': lambda x: _is_valid_stringfield(x, 0),
    'allowCallDirect': lambda x: _true_or_value_error(isinstance(x, bool)),
    'allowPersonalMeeting': lambda x: _true_or_value_error(isinstance(x, bool)),
    'locationTag': _is_valid_stringfield,
}


@six.python_2_unicode_compatible
class PortalMember(object):
    """
    PortalMember is a type-checking representation of the 'Member'
    class expected by the VidyoPortal Admin API.
    Here it is masquerading as a ``dict`` and can therefore be iterated
    upon and passed to the ``createMember()`` RPC function.
    Values are checked for sanity on __setattr__() by looking up their name in the
    ``VALIDATORS`` dictionary and running validation on them.

    ``ValueError`` or ``TypeError`` is raised on validation failure.

    The VidyoPortalUserService?wsdl does not define the 'Member' datatype so we
    can not use ``suds.client.factory`` methods to instantiate 'Member' objects.
    This class fulfills that lack, and enforces type-checking.
    """

    def __init__(self, **kwargs):
        super(PortalMember, self).__setattr__(
            'data',
            {
                'Language': 'en',
                'RoleName': 'Normal',
                'allowCallDirect': False,
                'allowPersonalMeeting': False,
                'description': '',
                'displayName': 'Anonymous',
                'emailAddress': '',
                'extension': '',
                'groupName': 'Default',
                'locationTag': 'Default',
                'name': '',
                'password': '',
                'proxyName': 'No Proxy'
            }
        )

        if kwargs.pop('validate', True):
            self.typechecker = VALIDATORS
            for key, val in kwargs.items():
                if key in self.data:
                    setattr(self, key, val)
        else:
            self.typechecker = None

    def __setattr__(self, attr, val):
        """
        __setattr__ is overidden to do type-checking conforming to the
        specifications of the VidyoPortal.  Setting an attribute causes the
        validator function to run when constructed with ``validate=True``.
        """
        if attr in self.data:
            if self.typechecker:
                self.typechecker[attr](val)
                self.data[attr] = val
            else:
                self.data[attr] = val
        else:
            super(PortalMember, self).__setattr__(attr, val)

    def validate(self):
        """
        Manual validation of all attrs to ensure that they will be acceptable
        for the VidyoPortalAdminService
        """
        for key, val in self.data.items():
            VALIDATORS[key](val)

    def __getattr__(self, attr):
        """look like a dict to anyone who's interested"""
        if attr in self.data:
            return self.data[attr]
        return object.__getattribute__(self, attr)

    def __str__(self):
        return str(self.data)

    def __iter__(self):
        try:
            return self.data.iteritems()
        except AttributeError:
            # python3
            return iter(self.data.items())

    def update(self, **kwargs):
        self.data.update(**{
            key: val for key, val in kwargs.items() if key in self.data.keys()}
        )

    @deprecated
    def update_existing(self, **kwargs):
        return self.update(**kwargs)
