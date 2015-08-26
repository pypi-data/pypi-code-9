import requests
import json
import os


headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer {0}'.format(os.environ.get('do_access_token', '')),
}


class UnexpectedStatusCodeException(Exception):
    pass


def print_r(r):
    if os.environ.get('do_api_debug', False) != 'true':
        return
    print r.status_code
    if r.status_code != 204:
        print json.dumps(r.json(), indent = 4)


def check_r(r, status_code):
    if r.status_code != status_code:
        raise UnexpectedStatusCodeException('expected {0}, got {1}'.format(status_code, r.status_code))


def api_request(method, path, **d):
    expected_status_code = d.pop('status_code')
    d['headers'] = headers
    r = method('https://api.digitalocean.com/v2/' + path, **d)
    print_r(r)
    check_r(r, expected_status_code)
    return r


def api_get(path, **d):
    return api_request(requests.get, path, **d)


def api_post(path, **d):
    return api_request(requests.post, path, **d)


def api_delete(path, **d):
    return api_request(requests.delete, path, **d)
