
import pytest
import time

from elogging.util import profile

@profile
def get_user(t):
    time.sleep(t)
    return 'Alice'

@profile
def get_tweet(t):
    time.sleep(t)
    return 'Announce a module "elogging"'

def test_profile():
    get_user(1)
    assert 1 == int(get_user.stats())
    get_tweet(2)
    assert 2 == int(get_tweet.stats())
    get_user(3)
    assert 3 == int(get_user.stats())

