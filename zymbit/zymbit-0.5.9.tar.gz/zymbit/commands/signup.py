import logging
import random

import sys

import requests

from zymbit.commands import Command
from zymbit.common.config import get_config, save_auth
from zymbit.util import validate_email


def random_string(length=20):
    chars = (
        'abcdefghijklmnopqrstuvwxyz'
        'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        '0123456789'
        '!@#$%^*|-+='
    )

    selected = []
    for _ in range(20):
        selected.append(random.choice(chars))

    return ''.join(selected)


class SignupCommand(Command):
    command_name = 'signup'
    api_endpoint = '/registration'

    @property
    def logger(self):
        return logging.getLogger(__name__)

    @classmethod
    def setup_parser(cls, parser):
        command_parser = super(SignupCommand, cls).setup_parser(parser)

        # use type kwarg to validate email address
        # http://stackoverflow.com/a/14117511/703144
        command_parser.add_argument('email', type=validate_email)

        return command_parser

    def run(self):
        # randomly generate a password
        password = random_string()

        params = {
            'email': self.args.email,
            'password': password,
        }

        config = get_config()
        api_url = config['cloud']['api_url']
        verify = config['cloud'].get('check_hostname', True)

        url = '{}{}'.format(api_url, self.api_endpoint)

        try:
            response = requests.post(url, data=params, verify=verify)
        except requests.ConnectionError, exc:
            self.logger.error('Unable to connect to url={}'.format(url))

            self.logger.exception(exc)
        else:
            try:
                response.raise_for_status()
            except requests.HTTPError:
                data = response.json()
                sys.exit(data)

            # save the login information
            auth_data = response.json()

            try:
                save_auth(auth_data, password)
            except requests.HTTPError:
                data = response.json()
                sys.exit(data)

            print 'You are signed up; check your email at {} for the verification key'.format(self.args.email)
