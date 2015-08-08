from libsousou.cli import Argument
from libsousou.cli import BaseCommand
from libsousou.cli.baseparser import BaseParser


class Command(BaseCommand):
    command_name = 'testcommand'
    help_text = 'This is a test command'
    args = [
        Argument('pos', help='a positional argument'),
        Argument('--named', help='a named argument')
    ]
    executed = False

    def handle(self, args):
        Command.executed = True
