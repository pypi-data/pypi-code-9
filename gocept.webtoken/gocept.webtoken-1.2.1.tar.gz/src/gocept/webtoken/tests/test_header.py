from gocept.webtoken import create_authorization_header, extract_token
import collections
import pytest


def test_header__create_authorization_header__1():
    """Function creates bearer header for a given webtoken dict."""
    key, value = create_authorization_header({'token': b'<TOKEN>'})
    assert 'Authorization' == key
    assert 'Bearer <TOKEN>' == value


def test_header__create_authorization_header__2():
    """Function creates bearer header for a given webtoken."""
    key, value = create_authorization_header(b'<TOKEN>')
    assert 'Authorization' == key
    assert 'Bearer <TOKEN>' == value


def test_header__extract_token__1():
    """`extract_token()` extracts token from given dict."""
    headers = dict(Authorization='Bearer <TOKEN>')
    assert b'<TOKEN>' == extract_token(headers)


def test_header__extract_token__2():
    """`extract_token()` extracts token from given value."""
    assert b'<TOKEN>' == extract_token('Bearer <TOKEN>')


def test_header__extract_token__3():
    """`extract_token()` allows scheme to be lower case."""
    assert b'<TOKEN>' == extract_token('bearer <TOKEN>')


def test_header__extract_token__4():
    """`extract_token()`  raises ValueError if Authorization key is missing."""
    with pytest.raises(ValueError) as err:
        extract_token({})
    assert 'Missing Authorization header' == str(err.value)


def test_header__extract_token__5():
    """`extract_token()`  raises ValueError on wrong Authorization scheme."""
    headers = dict(Authorization='Foobar <TOKEN>')
    with pytest.raises(ValueError) as err:
        extract_token(headers)
    assert 'Authorization scheme is not Bearer' == str(err.value)


def test_header__extract_token__6():
    """`extract_token()`  raises ValueError if scheme is missing."""
    headers = dict(Authorization='<TOKEN>')
    with pytest.raises(ValueError) as err:
        extract_token(headers)
    assert 'Authorization scheme is not Bearer' == str(err.value)


def test_header__extract_token__7():
    """`extract_token()` extracts token from given Mapping object."""
    class MyHeaders(collections.Mapping):
        """Example headers implementation based on `Mapping ."""

        def __init__(self, data):
            self.data = data

        def __getitem__(self, key):
            return self.data[key]

        def __iter__(self):
            return iter(self.data)

        def __len__(self):
            return len(self.data)

    headers = MyHeaders({'Authorization': 'Bearer <TOKEN>'})
    assert b'<TOKEN>' == extract_token(headers)
