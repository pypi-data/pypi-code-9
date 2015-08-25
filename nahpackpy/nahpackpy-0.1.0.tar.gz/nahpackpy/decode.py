# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""
Decode docs.
"""

from __future__ import absolute_import, unicode_literals, division

from collections import namedtuple

from .compat import PY3, PYPY
from .error import errcode_to_exc
from .ffi import ffi, libnahpack


__all__ = (
    'Headers',
    'Decoder',
)


Header = namedtuple('Header', ('name', 'value', ))

if PY3 and not PYPY:  # pragma: no cover
    Header.__doc__ = """
    Header is a `namedtuple` of `name` and `value`.

    .. py:attribute:: name bytes

    .. py:attribute:: value bytes
    """


class Headers(object):
    """
    Headers is an iterable of decoded :class:`.Header` objects.
    """

    __slots__ = ('_inner', 'decoded', )

    def __init__(self, decoded, num):
        self._inner = decoded
        tuples = []
        for idx in range(0, num):
            header = libnahpack.nahpack_get_header(decoded, idx)
            tuples.append(
                Header(
                    ffi.string(header.name, header.name_len),
                    ffi.string(header.value, header.value_len)
                )
            )
        self.decoded = tuple(tuples)

    def __del__(self):
        libnahpack.nahpack_headers_free(self._inner)

    def __len__(self):
        return len(self.decoded)

    def __getitem__(self, key):
        return self.decoded[key]

    def __iter__(self):
        return iter(self.decoded)

    def __repr__(self):
        return 'Headers(%s)' % ', '.join(
            [
                ('(%s, %s)' if PY3 else '("%s", "%s")') % each
                for each in self.decoded
            ]
        )

    __str__ = __repr__

    __unicode__ = __repr__


class Decoder(object):
    """
    Decoder contains the dynamic table and capacity setting
    for decompressing inbound headers.
    """

    __slots__ = ('_context', 'capacity')

    def __init__(self):
        self.capacity = 4096
        self._context = libnahpack.nahpack_context_new()

    def __del__(self):
        libnahpack.nahpack_context_free(self._context)

    def decode_block(self, block):
        """
        Decode a transmitted block and, if valid, return a :class:`.Headers`
        object containing the decoded headers.

        :param bytes headers: Block to decode. If a block is transmitted
            over multiple frames, the entire, merged block must be given.

        :rtype: :class:`.Headers`

        :raises:
            :class:`.InsufficientData`,
            :class:`.InvalidIndex`,
            :class:`.InvalidInteger`,
            :class:`.ExcessiveInteger`,
            :class:`.InvalidCompressedLiteral`,
            :class:`.IllegalEOS`,
            :class:`.SettingsSizeExceeded`

        """
        ffiblock = ffi.new('char[]', block)
        decoded = libnahpack.nahpack_headers_new(
            ffiblock,
            len(ffiblock) - 1,  # NUL
        )
        num = libnahpack.nahpack_decode_block(self._context, decoded)
        if num < 0:
            raise errcode_to_exc(num)
        return Headers(decoded, num)

    def set_capacity(self, capacity):
        """
        Set the maximum table capacity as set in a SETTINGS frame.

        :param int capacity: SETTINGS frame value.
        """
        libnahpack.nahpack_set_context_capacity(self._context, capacity)
        self.capacity = capacity
