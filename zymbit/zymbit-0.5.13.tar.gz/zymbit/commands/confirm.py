from __builtin__ import classmethod
import logging
import sys

import requests

from zymbit.commands import Command
from zymbit.util import ZymbitApi


class ConfirmCommand(Command):
    command_name = 'confirm'
    api_endpoint = '/registration/{}/confirm'

    @property
    def logger(self):
        return logging.getLogger(__name__)

    @classmethod
    def setup_parser(cls, parser):
        command_parser = super(ConfirmCommand, cls).setup_parser(parser)

        command_parser.add_argument('confirmation_code')

        return command_parser

    def run(self):
        api = ZymbitApi()
        endpoint = self.api_endpoint.format(self.args.confirmation_code)
        try:
            response = api.request('post', endpoint)
        except requests.ConnectionError, exc:
            sys.exit(exc)
        except requests.HTTPError:
            access_okay = False

            error_response = api.response
            if api.response.status_code == 404:
                response = api.request('get', '/zymbots')
                if response.status_code == 200:
                    access_okay = True
                else:
                    sys.exit('confirmation code not found, are you already confirmed?')

            if not access_okay:
                data = error_response.json()
                sys.exit(data)

        print 'Your email address is confirmed'
