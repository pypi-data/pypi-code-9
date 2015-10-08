import gocept.webtoken
import pkg_resources
import pytest
import zope.component


@pytest.yield_fixture(scope='module', autouse=True)
def import_keys():
    keys = gocept.webtoken.CryptographicKeys(
        pkg_resources.resource_filename('gocept.webtoken', 'testing/keys'),
        ['jwt-access', 'jwt-application'])
    zope.component.provideUtility(keys)
    yield
    zope.component.getSiteManager().unregisterUtility(keys)


@pytest.fixture(scope='function')
def token():
    return Token()


class Token:
    """Helper to create and decode tokens."""

    def create(self, key_name, subject, data=None, expires_in=None):
        from ..token import create_web_token
        return create_web_token(key_name, 'issuer', subject, expires_in, data)

    def decode(self, token, key_name, subject):
        from ..token import decode_web_token
        return decode_web_token(token['token'], key_name, subject)
