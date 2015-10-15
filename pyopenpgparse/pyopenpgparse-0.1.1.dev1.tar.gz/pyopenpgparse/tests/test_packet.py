#!/usr/bin/env python
import pytest

from pygcrypt.types.sexpression import SExpression

from pyopenpgparse.parser import ArmoryGenerator

@pytest.mark.parametrize("message", ['testdata/message_ok.asc'])
def test_parse_symmetric_encrypted_message(message):
    armor = ArmoryGenerator()
    with open(message, u'br') as stream:
        armor.dearmor(stream)
        for packet in armor.parse():
            assert isinstance(packet.sexp, SExpression)
            break
