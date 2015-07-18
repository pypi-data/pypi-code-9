# -*- coding: utf-8 -*-

__author__ = 'Vitalii Maslov'
__version__ = '1.0.0'
__email__ = 'me@pyvim.com'
__license__ = 'MIT'

import re

import requests

def authentication(login, password):
    """
    Authentication on vk.com.

    :param login: login on vk.com.
    :param password: password on vk.com.
    :returns: requests `Session`.
    """
    session = requests.Session()
    url = 'https://login.vk.com/?act=login&soft=1&utf8=1'
    data = {
        'act': 'login',
        'role': 'al_frame',
        'email': login,
        'pass': password
    }

    response = session.post(url, data=data)
    print(response.text)

    if 'q_hash' in response.url:
        return session
    return False

def oauth(session, app_id, scope, version):
    """
    OAuth on vk.com.

    :param session: `requests` Session class with authentication.
    :param app_id: application id.
    :param scope: authorization scope.
    :param version: API version.
    :returns: OAuth access token.
    """
    url = 'https://oauth.vk.com/authorize'
    params = {
        'client_id': app_id,
        'scope': scope,
        'redirect_uri': 'https://oauth.vk.com/blank.html',
        'display': 'mobile',
        'v': version,
        'response_type': 'token'
    }

    response = session.get(url, params=params)

    if 'access_token' not in response.url:
        url = re.search('action="(.*)"', response.text).group(1)
        response = session.post(url)

    if 'access_token' in response.url:
        token = re.search('token=(\w+)', response.url).group(1)
        return token

    return False
