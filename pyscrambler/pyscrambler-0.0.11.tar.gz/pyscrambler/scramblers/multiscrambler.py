# -*- coding: utf-8 -*-
from __future__ import absolute_import

from bitstring import BitArray
from oset import oset

from .basescrambler import BaseScrambler


class MultiScrambler(BaseScrambler):
    """
    MultiScrambler is an extended version of BaseScrambler that allows for
    scrambling data multiple times at different-sized chunks for improved
    cryptographic qualities.
    """
    def __init__(self, trans, keys):
        """
        Where trans is an array of integers specifying the size of chunks that
        the data should be split into for each iteration of scrambling.

        Where keys is an array of oset objects that specifies the order each
        iteration of scrambling should be re-arranged into.
        """
        if not hasattr(trans, '__iter__'):
            raise TypeError('Non-iterable type given for trans argument.')
        else:
            for tran in trans:
                if not isinstance(tran, int):
                    raise TypeError('Expected int for item in trans array.')
        if not hasattr(keys, '__iter__'):
            raise TypeError('Non-iterable type given for keys argument')
        else:
            for key in keys:
                if not isinstance(key, oset):
                    raise TypeError(('Expected oset object for item in keys '
                                     'array'))
        self.trans = trans
        self.keys = keys

    def scramble(self, data):
        """
        Where data is a bytearray object, split into chunks the size of
        self.trans, re-arrange according to self.keys order then convert back
        to bytearray and return this. Do this for each item in trans array and
        keys array.
        """
        if not isinstance(data, bytearray):
            raise TypeError(('Expected bytearray object for data argument, '
                             'received {}').format(type(data)))
        # convert to BitArray for easier chunking
        clear = BitArray(data)
        code = BitArray(clear)
        for index, tran in enumerate(self.trans):
            # get the key for this turn
            key = self.keys[index]
            code = super(MultiScrambler, self)._scramble(code, tran, key)
        return bytearray(code.tobytes())

    def unscramble(self, data):
        """
        Where data is a bytearray object, split into chunks the size of
        self.trans, re-arrange according to self.keys order then convert back
        to bytearray and return this. Do this for each item in trans array and
        keys array.
        """
        if not isinstance(data, bytearray):
            raise TypeError(('Expected bytearray object for data argument, '
                             'received {}').format(type(data)))
        # convert to BitArray for easier chunking
        code = BitArray(data)
        clear = BitArray(code)
        for index, tran in reversed(list(enumerate(self.trans))):
            # get the key for this turn
            key = self.keys[index]
            clear = super(MultiScrambler, self)._unscramble(clear, tran, key)
        return bytearray(clear.tobytes())
