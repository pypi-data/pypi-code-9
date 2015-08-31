# -*- coding: utf-8 -*-
"""Represent the PATCH method for HTTP 1.1.

The HTTP PATCH method as implemented in this module is defined in the
following document:

`IETF RFC 5789 <http://tools.ietf.org/html/rfc5789>`_

"""

# Support Python 2 & 3.
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from pyneric.future import *

from . import Method


PATCH = Method(
    'PATCH',
    "Modify the target resource with the request payload.",
    safe=False,
    idempotent=False,
    cacheable=False,
)
"""Representation of the HTTP 1.1 PATCH request method."""

CACHEABLE_PATCH = Method(
    PATCH.token,
    PATCH.description,
    safe=PATCH.safe,
    idempotent=PATCH.idempotent,
    cacheable=True,
)
"""Representation of the HTTP 1.1 cacheable PATCH request method.

Use this responsibly (pun intended, but also serious).  From the RFC:

    A response to this method is only cacheable if it contains explicit
    freshness information (such as an Expires header or
    "Cache-Control: max-age" directive) as well as the Content-Location
    header matching the Request-URI, indicating that the PATCH response
    body is a resource representation.  A cached PATCH response can
    only be used to respond to subsequent GET and HEAD requests; it
    MUST NOT be used to respond to other methods (in particular,
    PATCH).

"""
