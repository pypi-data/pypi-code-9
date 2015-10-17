# coding: UTF-8
# Copyright (C) 2007-2008, Stefan Schwarzer
# see the file LICENSE for the license of this software

"""
Tools for converting between unicode strings and byte strings.
"""

import urllib


# assume this encoding for all file names and their contents
DEFAULT_ENCODING = "UTF-8"

# the fallback encoding should be an 8-bit encoding
FALLBACK_ENCODING = "iso-8859-15"


class Error(Exception):
    pass


def encode(unicode_string):
    r"""Return a byte string for the given `unicode_string`. Use the
    `DEFAULT_ENCODING`.

    >>> import unicodedata
    >>> encode(u"abc")
    'abc'
    >>> encode(unicodedata.lookup('LATIN SMALL LETTER A WITH DIAERESIS')
    ... + u"bc")
    '\xc3\xa4bc'
    """
    if not isinstance(unicode_string, unicode):
        raise Error(u'argument "%r" isn\'t a unicode string' % unicode_string)
    return unicode_string.encode(DEFAULT_ENCODING, 'replace')

def decode(byte_string):
    r"""Return a unicode string for the given `byte_string`. If the
    argument can't be decoded, decode with the `FALLBACK_ENCODING`
    instead.

    >>> import unicodedata
    >>> s = "\xc3\xa4bc"  # UTF-8, umlaut encoded in two bytes
    >>> u = decode(s)
    >>> len(u), unicodedata.name(u[0])
    (3, 'LATIN SMALL LETTER A WITH DIAERESIS')

    >>> s = "\xe4bc"  # ISO-8859-1, umlaut encoded in one byte
    >>> u = decode(s)
    >>> len(u), unicodedata.name(u[0])
    (3, 'LATIN SMALL LETTER A WITH DIAERESIS')
    """
    if not isinstance(byte_string, str):
        raise Error(u'argument "%r" isn\'t a byte string' % byte_string)
    try:
        return byte_string.decode(DEFAULT_ENCODING)
    except UnicodeDecodeError:
        # 8-bit encoding, should always work
        return byte_string.decode(FALLBACK_ENCODING)

# these functions behave like the correspondingly named JavaScript functions
# see descriptions at
# https://developer.mozilla.org/en/Core_JavaScript_1.5_Reference/Global_Functions
# a "normal" `urllib.quote` result can't be decoded by JavaScript!
SAFE_URI_COMPONENT_CHARS = "-_.!~*'()"
SAFE_URI_CHARS = SAFE_URI_COMPONENT_CHARS + ";,/?:@&=+$#"

def encode_uri(uri):
    # see discussion starting at
    #  http://mail.python.org/pipermail/python-dev/2006-July/067248.html
    return urllib.quote(uri, SAFE_URI_CHARS)

def encode_uri_component(uri_component):
    return urllib.quote(uri_component, SAFE_URI_COMPONENT_CHARS)

def decode_uri(s):
    return urllib.unquote(s)

def decode_uri_component(s):
    # decoding is the same for both variants
    return decode_uri(s)

