from strawpoll import StrawpollAPIWriter

import requests
import pprint

BASE_URL = 'https://strawpoll.me'
API_PATH = 'api/v2/polls'
ENDPOINT = '/'.join([BASE_URL, API_PATH])
BAD_POLL = {
    'title': '',
    'options': [

    ],
    'multi': False,
    'permissive': False,
    'captcha': False
}
GOOD_POLL = {
    'title': 'A good pol;',
    'options': [
        "one",
        "two"
    ],
    'multi': False,
    'permissive': False,
    'captcha': False
}

request_good = StrawpollAPIWriter(GOOD_POLL)
request_bad = StrawpollAPIWriter(BAD_POLL)

response_good = request_good.post()
response_bad = request_bad.post()

pprint.pprint(response_good)
pprint.pprint(response_bad)


def _compare(x, y):
    if x is not None and y is not None:
        return x == y
    else:
        return False


def _has_same_title(a, b):
    try:
        return _compare(a.title, b.title)
    except AttributeError:
        return False


def _has_same_options(a, b):
    try:
        return _compare(a.options, b.options)
    except AttributeError:
        return False


def _has_same_multi(a, b):
    try:
        return _compare(a.multi, b.multi)
    except AttributeError:
        return False


def _has_same_permissive(a, b):
    try:
        return _compare(a.permissive, b.permissive)
    except AttributeError:
        return False


def _has_same_captcha(a, b):
    try:
        return _compare(a.captcha, b.captcha)
    except AttributeError:
        return False


def test_successfull_post_has_same_data_as_posted():
    assert(_has_same_title(request_good, response_good))
    assert(_has_same_options(request_good, response_good))
    assert(_has_same_multi(request_good, response_good))
    assert(_has_same_permissive(request_good, response_good))
    assert(_has_same_captcha(request_good, response_good))
