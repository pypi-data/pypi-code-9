import pytest


def create_token(key_name, subject, data=None, expires_in=None):
    from ..token import create_web_token
    return create_web_token(key_name, 'issuer', subject, expires_in, data)


def decode_token(token, key_name, subject):
    from ..token import decode_web_token
    return decode_web_token(token['token'], key_name, subject)


def test_token__decode_web_token__1():
    """Raises ValueError on invalid token."""
    with pytest.raises(ValueError) as err:
        decode_token({'token': 'asdf'}, 'jwt-application-public', 'asdf')
    assert 'Not enough segments' == str(err.value)


def test_token__decode_web_token__2():
    """Raises ValueError on wrong cryptographic key."""
    token = create_token('jwt-application-private', 'app')
    with pytest.raises(ValueError) as err:
        decode_token(token, 'jwt-access-public', 'app')
    assert 'Signature verification failed' == str(err.value)


def test_token__decode_web_token__3():
    """Raises ValueError on expired token."""
    token = create_token('jwt-access-private', 'app', expires_in=-1)
    with pytest.raises(ValueError) as err:
        decode_token(token, 'jwt-access-public', 'app')
    assert 'Signature has expired' == str(err.value)


def test_token__decode_web_token__4():
    """Raises ValueError on invalid subject."""
    token = create_token('jwt-access-private', 'app')
    with pytest.raises(ValueError) as err:
        decode_token(token, 'jwt-access-public', 'access')
    assert "Subject mismatch 'access' != 'app'" == str(err.value)


def test_token__decode_web_token__5():
    """Returns decoded token contend if valid."""
    token = create_token('jwt-access-private', 'app', data={'foo': 'bar'})
    decoded = decode_token(token, 'jwt-access-public', 'app')
    assert (
        sorted([u'iss', u'iat', u'data', u'sub', u'nbf']) ==
        sorted(decoded.keys()))
    assert 'issuer' == decoded['iss']
    assert {u'foo': u'bar'} == decoded['data']
    # iat, nbf and exp have been checked implicitly by validation upon
    # decoding


def test_token__cecode_web_token__1():
    """Create web token returns encoded token and token contents."""
    token = create_token('jwt-access-private', 'app', data={'foo': 'bar'})
    assert token['data'] == decode_token(token, 'jwt-access-public', 'app')
