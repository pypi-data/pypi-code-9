# encoding: utf-8

"""

Base/shared class or functions

release |release|, version |version|

.. versionadded:: 1.0

    Initial

Contents
--------

Classes:

* :class:`BaseEncoder`
* :class:`BaseDecoder`

Functions:

Variables:

Members
-------

"""

import re


class BaseEncoder(object):

    mapping = None
    encoding = 'utf-8'

    def __init__(self, mapping=None, encoding='utf-8', *args, **kwargs):

        self.mapping = mapping or self.mapping
        self.encoding = encoding or self.encoding

        if self.mapping is None:
            raise AttributeError("mapping should not be None")

    def encode(self, msg, *args, **kwargs):
        """enccode msg

        """
        msg = self.pre_encode(msg, *args, **kwargs)
        msg = self._encode(msg, *args, **kwargs)
        msg = self.post_encode(msg, *args, **kwargs)
        return msg

    def pre_encode(self, msg, *args, **kwargs):
        """ hook before encoding """
        return msg

    def _encode(self, msg, *args, **kwargs):
        ''' actual encode method '''
        _msg = ''

        try:
            for i, v in enumerate(msg.upper()):
                _msg += (self.mapping[v] if v in self.mapping else v)
        except KeyError:
            raise

        return _msg

    def post_encode(self, msg, *args, **kwargs):
        """ hook after encoding """
        return msg


class BaseDecoder(object):

    mapping = None
    encoding = 'utf-8'

    def __init__(self, mapping=None, encoding='utf-8', *args, **kwargs):

        self.mapping = mapping or self.mapping
        self.encoding = encoding or self.encoding

        if self.mapping is None:
            raise AttributeError("mapping should not be None")

    def decode(self, msg, *args, **kwargs):
        """enccode msg

        """
        msg = self.pre_decode(msg, *args, **kwargs)
        msg = self._decode(msg, *args, **kwargs)
        msg = self.post_decode(msg, *args, **kwargs)
        return msg

    def pre_decode(self, msg, *args, **kwargs):
        """ hook before decoding """
        return msg

    def _decode(self, msg, *args, **kwargs):
        ''' actual decode method '''

        try:
            for k, v in self.mapping.items():
                msg = re.sub(re.escape(k), v, msg)
        except KeyError:
            raise

        return msg

    def post_decode(self, msg, *args, **kwargs):
        """ hook after decoding """
        return msg
