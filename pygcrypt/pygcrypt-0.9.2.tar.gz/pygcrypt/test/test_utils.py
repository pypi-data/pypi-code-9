#!/usr/bin/env python

import pytest

from pygcrypt import utils

def test_radix64():
    assert utils.r64decode(utils.r64encode(b'This is a wonderfull world')) == b'This is a wonderfull world'

def test_keyderive(context):
    assert utils.key_derive("A passphrase is here!", "8bitsalt") == b'!\n\xe9qjQKK\x0c\xc2,\xad\x8b\x9c\x03O\xa2Apt\xda\x0c`[\xcf'
    with pytest.raises(Exception):
        # We should fail with this salt of len != 8 for the default algo
        utils.key_derive("yay, passphrase", "123")
