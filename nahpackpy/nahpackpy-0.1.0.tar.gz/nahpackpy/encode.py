# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""
Encode docs.
"""

from __future__ import absolute_import, unicode_literals, division

from .error import InvalidHeaders
from .ffi import ffi, libnahpack


__all__ = (
    'Encoder',
)


@ffi.callback('void(void *, char *const, size_t)')
def encode_callback(passthrough_ptr, result_buffer, length):
    res = ffi.from_handle(passthrough_ptr)
    buf = ffi.buffer(result_buffer, length)
    res[0:length] = buf[0:length]


class Encoder(object):
    """
    Encoder contains the dynamic table and size setting
    for compressing outbound headers.
    """

    __slots__ = ('_context', 'capacity')

    def __init__(self):
        self.capacity = 4096
        self._context = libnahpack.nahpack_context_new()

    def __del__(self):
        libnahpack.nahpack_context_free(self._context)

    def encode_block(self, headers):
        """
        Encode an iterable of headers and return the bytes.

        :param tuple headers: Iterable of
            `(name<bytes>, value<bytes>)` iterables.

        :rtype: bytes

        :raises:
            :class:`.InvalidHeaders`
        """
        try:
            header_dicts = [
                {
                    'name': ffi.new("char[]", header[0]),
                    'name_len': len(header[0]),
                    'value': ffi.new("char[]", header[1]),
                    'value_len': len(header[1]),
                    'compressable': True,
                }
                for header
                in headers
            ]
        except TypeError:
            raise InvalidHeaders('headers must be (bytes, bytes), not unicode')
        enc_headers = ffi.new('nahpack_header[]', header_dicts)

        buf = bytearray(4096)
        res = libnahpack.nahpack_encode_block(
            enc_headers,
            len(enc_headers),
            self._context,
            encode_callback,
            ffi.new_handle(buf),
        )
        return bytes(buf[0:res])

    def set_capacity(self, capacity):
        """
        Set the maximum table capacity as set in a SETTINGS frame.

        :param int capacity: SETTINGS frame value.
        """
        libnahpack.nahpack_set_context_capacity(self._context, capacity)
        self.capacity = capacity


