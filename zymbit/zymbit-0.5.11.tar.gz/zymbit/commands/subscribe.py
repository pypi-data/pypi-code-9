import logging

from zymbit.commands import Command
from zymbit.stream import Stream


class EchoStream(Stream):
    def handle(self, envelope):
        print envelope


class SubscribeCommand(Command):
    command_name = 'subscribe'

    @property
    def logger(self):
        return logging.getLogger(__name__)

    @classmethod
    def setup_parser(cls, parser):
        command_parser = super(SubscribeCommand, cls).setup_parser(parser)

        command_parser.add_argument('subscriptions', nargs='+')

        return command_parser

    def run(self):
        EchoStream(self.args.subscriptions).run()
