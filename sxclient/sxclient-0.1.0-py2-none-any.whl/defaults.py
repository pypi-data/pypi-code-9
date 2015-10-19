'''
Variables controlling the library's behaviour.

Copyright (c) 2015 Skylable Ltd.
License: Apache 2.0, see LICENSE for more details.

'''

VALID_ENCODED_KEY_LENGTH = 56
VALID_ENCODED_KEY_CHARACTERS = ('ABCDEFGHIJKLMNOPQRSTUVWXYZ'
                                'abcdefghijklmnopqrstuvwxyz'
                                '0123456789+/=')
VALID_DECODED_KEY_LENGTH = 42

FILTER_UUID_TO_NAME = {u'd5dbdf0afb174d1ba9ce4060317af5b5': u'zcomp',
                       u'7e7b7a8fe294458aa2abed8944ffce5c': u'undelete',
                       u'43122b8c56d146718500aa6831eb983c': u'attribs',
                       u'35a5404d15134009904c6ee5b0cd8634': u'aes256'}
FILTER_NAME_TO_UUID = {value: key for key, value
                       in FILTER_UUID_TO_NAME.iteritems()}
