# -*- coding: utf-8 -*-
"""Represent the Hypertext Transport Protocol 1.1 core standards.

This package module represents core HTTP, whereas additions and
extensions are represented in separate modules.

The standard as implemented in this module is defined in the following
documents:

* `IETF RFC 7230 <http://tools.ietf.org/html/rfc7230>`_
* `IETF RFC 7231 <http://tools.ietf.org/html/rfc7231>`_
* `IETF RFC 7232 <http://tools.ietf.org/html/rfc7232>`_
* `IETF RFC 7233 <http://tools.ietf.org/html/rfc7233>`_
* `IETF RFC 7234 <http://tools.ietf.org/html/rfc7234>`_
* `IETF RFC 7235 <http://tools.ietf.org/html/rfc7235>`_

This is far from complete and likely never will be, but it may be built
upon as needs arise.

"""

# Support Python 2 & 3.
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from pyneric.future import *

from collections import namedtuple


Method = namedtuple('Method', 'token description safe idempotent cacheable')
"""Class used to represent an HTTP 1.1 request method.

See
`Section 4 of RFC 7231 <http://tools.ietf.org/html/rfc7231#section-4>`_
for details.

"""


GET = Method(
    'GET',
    "Transfer a current representation of the target resource.",
    safe=True,
    idempotent=True,
    cacheable=True,
)
"""Representation of the HTTP 1.1 GET request method."""

HEAD = Method(
    'HEAD',
    "Same as GET, but only transfer the status line and header section.",
    safe=True,
    idempotent=True,
    cacheable=True,
)
"""Representation of the HTTP 1.1 HEAD request method."""

POST = Method(
    'POST',
    "Perform resource-specific processing on the request payload.",
    safe=False,
    idempotent=False,
    cacheable=True,
)
"""Representation of the HTTP 1.1 POST request method."""

PUT = Method(
    'PUT',
    "Replace all current representations of the target resource with the "
    "request payload.",
    safe=False,
    idempotent=True,
    cacheable=False,
)
"""Representation of the HTTP 1.1 PUT request method."""

DELETE = Method(
    'DELETE',
    "Remove all current representations of the target resource.",
    safe=False,
    idempotent=True,
    cacheable=False,
)
"""Representation of the HTTP 1.1 DELETE request method."""

CONNECT = Method(
    'CONNECT',
    "Establish a tunnel to the server identified by the target resource.",
    safe=False,
    idempotent=False,
    cacheable=False,
)
"""Representation of the HTTP 1.1 CONNECT request method."""

OPTIONS = Method(
    'OPTIONS',
    "Describe the communication options for the target resource.",
    safe=True,
    idempotent=True,
    cacheable=False,
)
"""Representation of the HTTP 1.1 OPTIONS request method."""

TRACE = Method(
    'TRACE',
    "Perform a message loop-back test along the path to the target resource.",
    safe=True,
    idempotent=True,
    cacheable=False,
)
"""Representation of the HTTP 1.1 TRACE request method."""

METHODS = set((
    GET,
    HEAD,
    POST,
    PUT,
    DELETE,
    CONNECT,
    OPTIONS,
    TRACE,
))
"""A set of all of the HTTP 1.1 request methods."""
