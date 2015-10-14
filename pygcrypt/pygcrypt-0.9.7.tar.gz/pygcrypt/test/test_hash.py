#!/usr/bin/env python

import pytest

from pygcrypt import hashcontext

def test_init(context):
    h = hashcontext.HashContext(algo='sha256')
    assert h.secure == True
    assert h.hmac == False
    h = hashcontext.HashContext(algo='sha256', secure=False, hmac=True)
    assert h.secure == False
    assert h.hmac == True

def test_valid(context):
    with pytest.raises(Exception):
        h = hashcontext.HashContext(algo='yadayada')

def test_getattr(context):
    h = hashcontext.HashContext(algo='sha256')
    assert h.algo == b'sha256'.upper()
    assert h.hashlen == 32

def test_enable(context):
    h = hashcontext.HashContext(algo='sha256')
    h.enable('sha512')
    
    with pytest.raises(Exception):
        h.enable('yadayada')

def test_setkey(context):
    h = hashcontext.HashContext(algo='sha256', hmac=True)
    assert h.hmac == True
    h.setkey(b'What a beautiful key')

def test_write(context):
    h = hashcontext.HashContext(algo='sha256')
    h.write("Let's write things to be hashed")

def test_read(context):
    h = hashcontext.HashContext(algo='sha256')
    h.write("Let's write things to be hashed")
    assert h.read() == b'\x1b>n\xb4\xa0\xc9]K\\,\xb2Fd\xcb\xae<.t\x08h\x91\xa3\xdeZ\x0c\xe6<\xc2$\x01!Q'

def test_reset(context):
    h = hashcontext.HashContext(algo='sha256')
    h.write('tototatatiti')
    one = h.read()
    h.reset()
    h.write('tototatatiti')
    assert one == h.read()

def test_copy(context):
    h = hashcontext.HashContext(algo='sha256')
    h.write('yadayada')
    h2 = h.copy()
    assert h.read() == h2.read()
