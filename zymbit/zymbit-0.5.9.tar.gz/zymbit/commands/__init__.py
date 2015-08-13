import argparse
import logging

import zymbit  # trigger setting up import hooks
import zymbit.common.config
from zymbit.commands.util import get_classes
from zymbit.logconfig import LOGLEVEL, config_logging


class Command(object):
    """
    Command subclass for all commands

    The get_classes() util will filter classes based on a subclass.
    This class should be used on all commands in order to include
    them.
    """
    command_name = 'subcommand'

    def __init__(self, parser, args):
        self.parser = parser
        self.args = args

    @classmethod
    def process_command(cls, package):
        parser = argparse.ArgumentParser()
        parser.add_argument('--logfile')  # default None
        parser.add_argument('--loglevel', '-l', default=LOGLEVEL)
        parser.add_argument('--config', '-c')

        subparser = parser.add_subparsers(dest='action')

        commands = dict([(x.command_name, x) for x in get_classes(package, cls)])
        for command in commands.values():
            command.setup_parser(subparser)

        args = parser.parse_args()
        if args.config:
            zymbit.common.config.CONFIG_PATH = args.config

        config_logging(args.logfile, args.loglevel)

        logger = logging.getLogger(__name__)

        logger.debug('action={}'.format(args.action))
        try:
            action_cls = commands[args.action]
        except KeyError:
            return 'unknown action={}'.format(args.action)

        return action_cls(parser, args).run()

    @classmethod
    def setup_parser(cls, parser):
        command_parser = parser.add_parser(cls.command_name)

        return command_parser

    def run(self):
        print 'run stub for command_name={}'.format(self.command_name)
