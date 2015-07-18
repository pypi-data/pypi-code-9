"""Pepa is a stupid simple CLI tool to call the Salt HTTP API remotely.

Usage:
  peppa <target> <function> [ARGUMENTS ...]
  peppa (-h | --help)
  peppa --version

"""
__version__ = '0.1'

import os
import json
import requests
from docopt import docopt

requests.packages.urllib3.disable_warnings()

class PeppaError(Exception):
    pass


class Peppa(object):
    def __init__(self, host, username, password, auth='ldap'):
        self.host = host
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.post({'username': username, 'password': password, 'eauth': auth}, uri='/login')

    def post(self, payload, uri='/'):
        url = '{}{}'.format(self.host, uri)
        response = self.session.post(url, data=payload, verify=False)
        if response.ok:
            return response.json()
        ret = response.status_code
        if ret == 401 and uri == '/login':
            raise PeppaError('Invalid login: {}'.format(self.username))
        else:
            raise PeppaError('POST request failed. Code: {}. Reason: {}'.format(ret, response.reason))

    def run(self, function, target, arg=None):
        if 'G@' in target:
            target = target.strip('G@')
            ret = self.post({'client': 'local', 'tgt': target, 'fun': function, 'arg': arg, 'expr_form': 'grain'})
        else:
            ret = self.post({'client': 'local', 'tgt': target, 'fun': function, 'arg': arg})
        return ret.get('return', [])


def print_json(response, indent=4):
    print(json.dumps(response, indent=indent))


def get_environment():
    env = {}
    env['host'] = os.environ.get('SALT_HOST')
    env['user'] = os.environ.get('SALT_USER')
    env['password'] = os.environ.get('SALT_PASSWORD')
    env['eauth'] = os.environ.get('SALT_EAUTH', 'ldap')
    if not env['host'] or not env['user'] or not env['password']:
        raise PeppaError('Environment variable(s) SALT_HOST, SALT_USER, or SALT_PASSWORD not set.')
    return env

def main():
    environment = get_environment()
    arguments = docopt(__doc__, version='Pepa version {}'.format(__version__))
    function = arguments.get('<function>', None)
    target = arguments.get('<target>', None)
    args = ' '.join(arguments.get('ARGUMENTS'))
    if not args:
        args = None

    salt = Peppa(environment['host'], environment['user'], environment['password'], environment['eauth'])
    print_json(salt.run(function=function, target=target, arg=args))


if __name__ == '__main__':
    main()
