# -*- coding: utf-8 -*-
from __future__ import absolute_import

from bitstring import BitArray
from oset import oset

from ..binary import bits_to_group
from ..rearrange import re_arrange, reverse_order


class BaseScrambler(object):
    """
    BaseScrambler is the base class for creating different scrambling systems
    using this module.
    """
    def __init__(self, trans, key):
        """
        Where trans is an integer specifying the size of chunks (in bits) that
        the input data should be broken into before re-ordering the data.
        Where key is an oset (ordered set) object containing the desired order
        that the data should be re-arranged into.
        """
        if isinstance(trans, int):
            self.trans = trans
        else:
            raise TypeError(
                'Expected int for trans argument, received {}'.format(
                    type(trans)))
        if isinstance(key, oset):
            self.keys = key
        else:
            raise TypeError(
                'Expected oset object for key argument, received {}'.format(
                    type(key)))

    def _scramble(self, clear, width, key):
        """
        Lower-level plumbing method used by the scramble function.

        This accepts clear as a BitArray, width as an integer and key as any
        array-type and re-orders the data after splitting it into chunks of
        given size.

        This is here to make it easier to override this class.
        """
        # get length in bits
        size = len(clear)
        # split up into chunks of size given by trans
        chunks = bits_to_group(clear, width)
        # re-arrange these chunks according to key
        jumbled = re_arrange(chunks, key)
        # convert back to one BitArray (get first and only item out of list)
        code = bits_to_group(jumbled, size)[0]
        return code

    def scramble(self, data):
        """
        Where data is a bytearray object, split into chunks the size of
        self.trans, re-arrange according to self.keys order then convert back
        to bytearray and return this.
        """
        if not isinstance(data, bytearray):
            raise TypeError(('Expected bytearray object for data argument, '
                             'received {}').format(type(data)))
        # convert to BitArray for easier chunking
        clear = BitArray(data)
        code = self._scramble(clear, self.trans, self.keys)
        return bytearray(code.tobytes())

    def _unscramble(self, code, width, key):
        """
        Lower-level plumbing method used by the unscramble function.

        This accepts code as a BitArray, width as an integer and key as any
        array-type and re-orders the data after splitting it into chunks of
        given size.

        This is here to make it easier to override this class.
        """
        # get length in bits
        size = len(code)
        # split up into chunks of size given by trans
        chunks = bits_to_group(code, width)
        # get the inverse of the key
        i_key = reverse_order(key)
        # re-arrange these chunks according to key
        jumbled = re_arrange(chunks, i_key)
        # convert back to one BitArray (get first and only item out of list)
        clear = bits_to_group(jumbled, size)[0]
        return clear

    def unscramble(self, data):
        """
        Where data is a bytearray object, split into chunks the size of
        self.trans, re-arrange according to self.keys inverse order then
        convert back to bytearray and return this. (Achieves the opposite of
        scramble method).
        """
        if not isinstance(data, bytearray):
            raise TypeError(('Expected bytearray object for data argument, '
                             'received {}').format(type(data)))
        # convert to BitArray for easier chunking
        code = BitArray(data)
        clear = self._unscramble(code, self.trans, self.keys)
        return bytearray(clear.tobytes())
