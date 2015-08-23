import getpass
import logging

import sys

import requests

from zymbit.commands import Command
from zymbit.common.config import get_config, save_auth
from zymbit.util import validate_email


class LoginCommand(Command):
    command_name = 'login'
    api_endpoint = '/members/login'

    @property
    def logger(self):
        return logging.getLogger(__name__)

    @classmethod
    def setup_parser(cls, parser):
        command_parser = super(LoginCommand, cls).setup_parser(parser)

        # use type kwarg to validate email address
        # http://stackoverflow.com/a/14117511/703144
        command_parser.add_argument('email', type=validate_email)

        return command_parser

    def run(self):
        password = getpass.getpass()

        params = {
            'username': self.args.email,
            'password': password,
        }

        config = get_config()
        api_url = config.lookup('cloud.api_url')
        verify = config.lookup('cloud.check_hostname')

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

            save_auth(response.json(), password)
