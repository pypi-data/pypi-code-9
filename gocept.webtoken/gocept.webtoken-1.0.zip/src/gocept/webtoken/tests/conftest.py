import gocept.webtoken.keys
import pkg_resources
import pytest
import zope.component


@pytest.yield_fixture(scope='module', autouse=True)
def import_keys():
    keys = gocept.webtoken.keys.CryptographicKeys(
        pkg_resources.resource_filename('gocept.webtoken', 'testing/keys'),
        ['jwt-access', 'jwt-application'])
    zope.component.provideUtility(keys)
    yield
    zope.component.getSiteManager().unregisterUtility(keys)
