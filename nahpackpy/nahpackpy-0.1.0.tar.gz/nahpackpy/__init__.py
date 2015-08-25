# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""
nahpackpy is an HTTP/2
`RFC 7541 HPACK <https://www.rfc-editor.org/rfc/rfc7541.txt>`_ library. It
wraps the Rust `nahpack
<https://github.com/ijl/nahpack>`_ library.


>>> from nahpackpy import Decoder
>>> decoder = Decoder()
>>> headers = decoder.decode_block(
        b'\\x82\\x86\\x84A\\x8c\\xf1\\xe3\\xc2\\xe5'
        b'\\xf2:k\\xa0\\xab\\x90\\xf4\\xff'
    )
>>> for header in headers:
        print(header)
Header(name=b':method', value=b'GET')
Header(name=b':scheme', value=b'http')
Header(name=b':path', value=b'/')
Header(name=b':authority', value=b'www.example.com')


>>> from nahpackpy import Encoder
>>> encoder = Encoder()
>>> encoder.encode_block((
        (b':method', b'GET'),
        (b':scheme', b'http'),
        (b':path', b'/'),
        (b':authority', b'www.example.com'),
    ))
b'\\x82\\x86\\x84A\\x8c\\xf1\\xe3\\xc2\\xe5\\xf2:k\\xa0\\xab\\x90\\xf4\\xff'

"""

from __future__ import absolute_import, unicode_literals, division


from .decode import (
    Decoder,
    Header,
    Headers,
)
from .encode import(
    Encoder,
)
from .error import (
    ExcessiveInteger,
    HpackDecodeError,
    IllegalEOS,
    InsufficientData,
    InvalidCompressedLiteral,
    InvalidHeaders,
    InvalidIndex,
    InvalidInteger,
    NahpackError,
    SettingsSizeExceeded,
)


__all__ = (
    'Decoder',
    'ExcessiveInteger',
    'Header',
    'Headers',
    'HpackDecodeError',
    'IllegalEOS',
    'InsufficientData',
    'InvalidCompressedLiteral',
    'InvalidHeaders',
    'InvalidIndex',
    'InvalidInteger',
    'NahpackError',
    'SettingsSizeExceeded',
    '__version__',
)


__version__ = '0.1.0'
