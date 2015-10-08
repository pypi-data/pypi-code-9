import gocept.webtoken.keys
import os.path
import shutil
import tempfile
import pytest


@pytest.yield_fixture(scope='function')
def keys_dir():
    keys_dir = tempfile.mkdtemp()
    yield keys_dir
    shutil.rmtree(keys_dir)


def test_keys__CryptographicKeys__1(keys_dir):
    """Key can be retrieved."""
    with open(os.path.join(keys_dir, 'jwt-access'), 'w') as f:
        f.write('secret')
    ck = gocept.webtoken.keys.CryptographicKeys(
        keys_dir, ['jwt-access'])
    assert 'secret' == ck['jwt-access-private']


def test_keys__CryptographicKeys__2(keys_dir):
    """Raises keyerror for unknown name."""
    ck = gocept.webtoken.keys.CryptographicKeys(
        keys_dir, ['jwt-access'])
    with pytest.raises(KeyError):
        ck['jwt-access-private']
