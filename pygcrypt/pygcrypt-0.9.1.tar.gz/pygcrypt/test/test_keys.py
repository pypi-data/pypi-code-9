#!/usr/bin/env python
from hashlib import sha256

import pytest

from pygcrypt.types.key import Key
from pygcrypt.utils import create_keys, randomize

def test_generate_keys(context):
    (priv, pub) = create_keys()
    assert isinstance(priv, Key)
    assert isinstance(pub, Key)

def test_keylen(context, private, public):
    assert len(private) == 4096
    assert len(public) == 4096

def test_sanity(context, private, public):
    assert private.issane() == True
    assert public.issane() == False

def test_algo(context, private, public):
    assert private.algo == u'rsa'
    assert public.algo == u'rsa'
    assert private.sign == True
    assert public.sign == True
    assert private.encr == True
    assert public.encr == True

def test_encryption(context, private, public):
    data = randomize(1024)
    assert private.decrypt(public.encrypt(data)) == data
    with pytest.raises(NotImplementedError):
        private.encrypt(data)
        public.decrypt(data)

def test_sign(context, private, public):
    hashing = sha256()
    hashing.update(b"Test data inserted")
    data = hashing.digest()
    with pytest.raises(NotImplementedError):
        public.makesign(data)

    sig = private.makesign(data)
    assert str(sig) == '(sig-val \n (rsa \n  (s #0DB6FD3B8915538E0C3619B32F47BBB2990E36F3E0ACBBA80E58BF317079928575EB06ED86247FD988A25F906BC4547983422DF30ACB64DE416D1144EEAEC08AD8DCDBA5E7A21956CECE6549CBBFA5B1D8E80994EAAEA266C4FEEBD7A613BDA1636487FA4F3FED102BF79779B8B6056F02D76F79BE96F64B555B578A0D8816535C2F6915D88ADE601FDD5D03862CB8240C4DA4A66AAE510B995EB5C76D6B62867FBB27D1BBEFE4A5BA77D0357035873F189B2FFE718F3BD164ACCCB5355D316C1A80B8BFF324AAB148854D4E1F40DF224DF7DFD7ADA056D343A0B81F9E6DCA6AD9C92924BD36C6C2D7688C94EC8DB45F3B3E38BFCA1B7475E29BF9442DCDEC154AD816AFEC1F7EE23A9228E40DB20248951FE2CE6E4AF9C546C7C108A862B58C99BD70AE72D73A8BCA00CC8A4501DC7FF5EEA7533BC065454FDFB270242DE7981B050DAFBE682A9F498F445AB6EA1ED20B1AF5BFBEE646214DF2CC214E6D3B6E59925600CDED856A49C0F5899669107A5D957E675BC94A53C32E476CE64B0DB77DDB4320179B5D36682F017FE9D8FA5D18A9C9955210F60AA4A18737AECAF9CA2DC9D938A1F73ECF274276FE3F8B9BC4879B75617F2E7AD8485FB71C7B10B2F0DCE6F2F0CE3FF1303145B7D11EE281B6A18A6F02B8E787A4956046BBE5AC5E47BF695712BAE9FC32A8881CB53D8881973B6C70AA648289A5DDB98EFF5C14A061#)\n  )\n )\n'
    assert public.verify(sig, data) == True
    with pytest.raises(NotImplementedError):
        private.verify(sig, data)
