import logging

from zymbit.commands import Command
from zymbit.commands.util import filter_parser_args
from zymbit.tunnel import Tunnel


class TunnelCommand(Command):
    command_name = 'tunnel'

    @classmethod
    def setup_parser(cls, parser):
        command_parser = super(TunnelCommand, cls).setup_parser(parser)

        command_parser.add_argument('--user')
        command_parser.add_argument('--host')
        command_parser.add_argument('--identity-file')
        command_parser.add_argument('--ssh-port', type=int)
        command_parser.add_argument('--port', type=int)

        return command_parser

    @property
    def logger(self):
        return logging.getLogger(__name__)

    def run(self):
        parser_args = filter_parser_args(self.args)

        self.logger.info('parser_args={}'.format(parser_args))

        tunnel = Tunnel(**parser_args)

        try:
            while True:
                tunnel.check()
        except KeyboardInterrupt:
            tunnel.close()
