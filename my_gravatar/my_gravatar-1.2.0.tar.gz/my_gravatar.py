__author__ = 'WelserJr'

"""" This is the gravatar module and it provides data from Gravatar. """

import requests
import json
from hashlib import md5


def gravatar(email):
    if email:
        email_code = md5(email.encode('utf-8')).hexdigest()
        url_json = 'http://www.gravatar.com/{}.json'.format(email_code)
        response = requests.get(url_json)
        data_response = json.loads(response.text)
        d = data_response['entry'][0]
        data = {
            'profile_url': validate(d, 'profileUrl'),
            'username': validate(d, 'preferredUsername'),
            'img': validate(d, 'thumbnailUrl'),
            'name': '{} {}'.format(validate(d['name'], 'givenName'), validate(d['name'], 'familyName')),
            'full_name': validate(d['name'], 'formatted'),
            'city': validate(d, 'currentLocation')
        }
        return data
    else:
        return None


def validate(d, key):
    if key in d:
        return d[key]
    else:
        return ""
