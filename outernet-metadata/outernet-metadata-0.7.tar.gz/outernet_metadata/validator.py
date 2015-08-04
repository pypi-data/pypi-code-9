"""
Validator to use a library

Copyright 2015, Outernet Inc.
Some rights reserved.

This software is free software licensed under the terms of GPLv3. See COPYING
file that comes with the source code, or http://www.gnu.org/licenses/gpl.txt.
"""

import validators

from . import values


VALIDATOR = validators.spec_validator(
    values.SPECS, key=lambda k: lambda obj: obj.get(k))


def validate(data, broadcast=False):
    """ Validates data

    When ``broadcast`` flag is ``True``, then the placeholder value for
    ``broadcast`` is not allowed.
    """
    res = VALIDATOR(data)
    if res:
        return res
    # Strict checking for broadcast
    if broadcast:
        if data['broadcast'] == '$BROADCAST':
            # Not allowing placeholders in strict mode
            raise ValueError('broadcast date cannot be a placeholder',
                             'broadcast_strict')
    # Additional validation that cannot be done using the specs
    if 'publisher' not in data:
        return {}
    return {}
