# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import absolute_import, unicode_literals, division


__all__ = (
    'errcode_to_exc',
    'ExcessiveInteger',
    'HpackDecodeError',
    'IllegalEOS',
    'InsufficientData',
    'InvalidCompressedLiteral',
    'InvalidHeaders',
    'InvalidIndex',
    'InvalidInteger',
    'NahpackError',
    'SettingsSizeExceeded',
)


class NahpackError(Exception):
    """
    nahpackpy captures all exceptions to raise NahpackError.

    Every other exception is a descendant of NahpackError.
    """


class HpackDecodeError(NahpackError):
    """
    nahpackpy captures all decoding exceptions to raise HpackDecodeError.
    """


class InsufficientData(HpackDecodeError):
    """
    The header block ends prematurely.
    """


class InvalidIndex(HpackDecodeError):
    """
    There was reference to an indexed header that is not in the table.
    """


class InvalidInteger(HpackDecodeError):
    """
    An integer could not be decoded.
    """


class ExcessiveInteger(HpackDecodeError):
    """
    This library's limit of an integer being at most 4 bytes was exceeded.
    """


class InvalidCompressedLiteral(HpackDecodeError):
    """
    The compressed literal could not be decoded.
    """


class IllegalEOS(HpackDecodeError):
    """
    EOS symbol was unexpectedly found in a compressed literal.
    """


class SettingsSizeExceeded(HpackDecodeError):
    """
    Header block gave a value for table resize that exceeds the value
    set by a settings frame.
    """


class InvalidHeaders(NahpackError):
    """
    The headers given for encoding were not of the type expected.
    """



ERRCODE_MAP = {
    -1: InsufficientData,
    -2: InvalidIndex,
    -3: InvalidInteger,
    -4: ExcessiveInteger,
    -5: InvalidCompressedLiteral,
    -6: IllegalEOS,
    -7: SettingsSizeExceeded,
}


def errcode_to_exc(code):
    try:
        return ERRCODE_MAP[code]()
    except KeyError:
        return HpackDecodeError()
