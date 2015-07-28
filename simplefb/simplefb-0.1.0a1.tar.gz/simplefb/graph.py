# -*- coding: utf-8 -*-

import urllib.parse
import urllib.request
import json

FB_API_HOST = 'https://graph.facebook.com'


def _api(endpoint, method, params, data=None, ver='v2.4'):
    url_params = urllib.parse.urlencode(params)
    url = '%s%s?%s' % (FB_API_HOST, endpoint, url_params)
    request = urllib.request.Request(url=url, data=data, method=method)
    request.add_header(key='facebook-api-version', val=ver)
    return urllib.request.urlopen(request).read().decode('utf-8')


def api(endpoint, method, params, data=None, ver='v2.4'):
    return json.loads(_api(endpoint, method, params, data, ver))


def fb_exchange_token(app_id, app_secret, short_lived_token):
    endpoint = '/oauth/access_token'
    params = {
        'grant_type': 'fb_exchange_token',
        'client_id': app_id,
        'client_secret': app_secret,
        'fb_exchange_token': short_lived_token,
    }
    return urllib.parse.parse_qs(_api(endpoint, 'GET', params))


def me(access_token):
    return api('/me', 'GET', {'access_token': access_token})
