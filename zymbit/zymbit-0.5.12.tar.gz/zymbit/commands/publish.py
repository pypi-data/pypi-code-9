import json
import logging

from zymbit.client import Client
from zymbit.commands import Command


class PublishCommand(Command):
    command_name = 'publish'

    @property
    def logger(self):
        return logging.getLogger(__name__)

    @classmethod
    def setup_parser(cls, parser):
        command_parser = super(PublishCommand, cls).setup_parser(parser)

        command_parser.add_argument('--route', default='data')
        command_parser.add_argument('key')
        command_parser.add_argument('value', help='JSON encoded, e.g. "3" is an int \'"3"\' is a string')

        return command_parser

    def run(self):
        client = Client()
        value = json.loads(self.args.value)

        client.send(self.args.route, {'key': self.args.key, 'value': value})

        none_count = 0
        while True:
            data = client.recv()
            if data is None:
                none_count += 1
                if none_count > 10:
                    break
            else:
                print data
