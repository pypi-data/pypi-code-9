import pytest


def test_token__decode_web_token__1(token):
    """Raises ValueError on invalid token."""
    with pytest.raises(ValueError) as err:
        token.decode({'token': 'asdf'}, 'jwt-application-public', 'asdf')
    assert 'Not enough segments' == str(err.value)


def test_token__decode_web_token__2(token):
    """Raises ValueError on wrong cryptographic key."""
    token_dict = token.create('jwt-application-private', 'app')
    with pytest.raises(ValueError) as err:
        token.decode(token_dict, 'jwt-access-public', 'app')
    assert 'Signature verification failed' == str(err.value)


def test_token__decode_web_token__3(token):
    """Raises ValueError on expired token."""
    token_dict = token.create('jwt-access-private', 'app', expires_in=-1)
    with pytest.raises(ValueError) as err:
        token.decode(token_dict, 'jwt-access-public', 'app')
    assert 'Signature has expired' == str(err.value)


def test_token__decode_web_token__4(token):
    """Raises ValueError on invalid subject."""
    token_dict = token.create('jwt-access-private', 'app')
    with pytest.raises(ValueError) as err:
        token.decode(token_dict, 'jwt-access-public', 'access')
    assert "Subject mismatch 'access' != 'app'" == str(err.value)


def test_token__decode_web_token__5(token):
    """Returns decoded token contend if valid."""
    token_dict = token.create('jwt-access-private', 'app', data={'foo': 'bar'})
    decoded = token.decode(token_dict, 'jwt-access-public', 'app')
    assert (
        sorted([u'iss', u'iat', u'data', u'sub', u'nbf']) ==
        sorted(decoded.keys()))
    assert 'issuer' == decoded['iss']
    assert {u'foo': u'bar'} == decoded['data']
    # iat, nbf and exp have been checked implicitly by validation upon
    # decoding


def test_token__create_web_token__1(token):
    """Create web token returns encoded token and token contents."""
    token_dict = token.create('jwt-access-private', 'app', data={'foo': 'bar'})
    assert token_dict['data'] == token.decode(
        token_dict, 'jwt-access-public', 'app')
