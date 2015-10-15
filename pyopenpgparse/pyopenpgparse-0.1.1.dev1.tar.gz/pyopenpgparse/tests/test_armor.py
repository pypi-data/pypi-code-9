#!/usr/bin/env python
import os.path

import pytest

from pyopenpgparse.parser import ArmoryGenerator, MalformedArmorException, ParseException, ChecksumException

"""
Let's test for armor parsing. it is based on RADIX 64 and needs a specific
CRC24 to works.

There's also a specific mode where some data are not in base 64 (in signature
of plain text system).
"""

@pytest.mark.parametrize("message, expected", [('testdata/message_ok.asc', 'MESSAGE')
                                    , ('testdata/public_key_block_ok.asc', 'PUBLIC KEY BLOCK')
                                    , ('testdata/private_key_block_ok.asc', 'PRIVATE KEY BLOCK')
                                    , ('testdata/multipart_message_ok.asc', 'MESSAGE')
                                    , ('testdata/part_message_ok.asc', 'MESSAGE')
                                    , ('testdata/clear_sign_ok.asc', 'SIGNED MESSAGE')
                                    , ('testdata/signature_ok.asc', 'SIGNATURE')])
def test_armor_integrity_ok(message, expected):
    """
    We want to test if the envelope is OK. Envelopes are extracted from
    messages given as a parameters.
    """
    with open(message, u'br') as stream:
        armor = ArmoryGenerator()
        armor.dearmor(stream)
        assert armor.type == expected

@pytest.mark.parametrize("message", ['testdata/armor_head_tail_mismatch.asc'
                                    , 'testdata/armor_head_type_unknown.asc'
                                    , 'testdata/armor_head_malformed.asc'])
def test_armor_integrity_ko(message):
    with pytest.raises(MalformedArmorException):
        with open(message, u'br') as stream:
            armor = ArmoryGenerator()
            armor.dearmor(stream)

@pytest.mark.parametrize("message", ['testdata/message_ok.asc'
                                    , 'testdata/part_message_ok.asc'])
def test_armor_headers_ok(message):
    with open(message, u'br') as stream:
        armor = ArmoryGenerator()
        armor.dearmor(stream)
        assert armor.headers['Version'] == 'GnuPG v2'
        if armor.multipart and armor.part_total != None:
            assert 'MessageID' in armor.headers

@pytest.mark.parametrize('message', ['testdata/headers_invalid.asc'
                                    , 'testdata/headers_messageid_missing.asc'
                                    , 'testdata/headers_messageid_tooshort.asc'
                                    , 'testdata/headers_messageid_ko.asc'])
def test_armor_headers_ko(message):
    with pytest.raises(ParseException):
        with open(message, u'br') as stream:
            armor = ArmoryGenerator()
            armor.dearmor(stream)

@pytest.mark.parametrize('message', ['testdata/clear_sign_ok.asc'])
def test_cleartext(message):
    with open(message, u'br') as stream:
        armor = ArmoryGenerator()
        armor.dearmor(stream)
        assert armor.clear_text == u'test\n'

@pytest.mark.parametrize("message", ['testdata/message_ok.asc'
                                    , 'testdata/public_key_block_ok.asc'
                                    , 'testdata/private_key_block_ok.asc'
                                    , 'testdata/multipart_message_ok.asc'
                                    , 'testdata/part_message_ok.asc'
                                    , 'testdata/clear_sign_ok.asc'
                                    , 'testdata/signature_ok.asc'])
def test_radix64_crc(message):
    with open(message, u'br') as stream:
        armor = ArmoryGenerator()
        armor.dearmor(stream)
        assert armor.verify() == True

@pytest.mark.parametrize("message", ['testdata/crc_missing.asc'
                                    , 'testdata/crc_bad.asc'])
def test_radix64_crc_ko(message):
    with pytest.raises(ChecksumException):
        with open(message, u'br') as stream:
            armor = ArmoryGenerator()
            armor.dearmor(stream)
            armor.verify()

@pytest.mark.parametrize("message", ['testdata/message_ok.asc'
                                    , 'testdata/public_key_block_ok.asc'
                                    , 'testdata/private_key_block_ok.asc'
                                    , 'testdata/multipart_message_ok.asc'
                                    , 'testdata/part_message_ok.asc'
                                    , 'testdata/clear_sign_ok.asc'
                                    , 'testdata/signature_ok.asc'])
def test_radix64_crc(message):
    with open(message, u'br') as stream:
        armor = ArmoryGenerator()
        armor.dearmor(stream)
        armor.tobinary()

@pytest.mark.parametrize("message", ['testdata/message_ok.asc'
                                    , 'testdata/public_key_block_ok.asc'
                                    , 'testdata/private_key_block_ok.asc'
                                    , 'testdata/multipart_message_ok.asc'
                                    , 'testdata/part_message_ok.asc'
                                    , 'testdata/clear_sign_ok.asc'
                                    , 'testdata/signature_ok.asc'])
def test_armor_generate(message):
    with open(message, u'br') as inputstream:
        armor = ArmoryGenerator()
        armor.dearmor(inputstream)
        binary = armor.tobinary()
        if armor.clearsign:
            clear_text = armor.clear_text
            armor.clear_text = u''
            out = armor.armor(binary, clear_text)
        else:
            out = armor.armor(binary)
        assert armor.headers['Version'] == u'Python OpenPGPParser'
        assert armor.verify() == True
        if armor.clearsign:
            assert armor.clear_text == clear_text
        for line in out:
            assert len(line) <= 74
