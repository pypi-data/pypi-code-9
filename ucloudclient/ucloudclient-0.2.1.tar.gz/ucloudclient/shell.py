#!/usr/bin/python
'''
Command line interface for ucloud
'''
from __future__ import print_function
import argparse
import logging
import os
import sys

import six

from api import shell_action
from utils import encodeutils
from utils import shell_utils
import client
import uexceptions


logger = logging.getLogger(__name__)


class UcloudClientArgumentParser(argparse.ArgumentParser):
    '''
    ucloud parser
    '''

    def __init__(self, *args, **kwargs):
        super(UcloudClientArgumentParser, self).__init__(*args, **kwargs)

    def error(self, message):
        '''error(message: string)

        Prints a usage message incorporating the message to stderr and
        exits.
        '''
        self.print_usage(sys.stderr)
        choose_from = ' (choose from'
        progparts = self.prog.partition(' ')
        self.exit(2, ("error: %(errmsg)s\nTry '%(mainp)s help %(subp)s'"
                      " for more information.\n") %
                  {'errmsg': message.split(choose_from)[0],
                   'mainp': progparts[0],
                   'subp': progparts[2]})

    def _get_option_tuples(self, option_string):
        '''returns (action, option, value) candidates for an option prefix

        Returns [first candidate] if all candidates refers to current and
        deprecated forms of the same options: "nova boot ... --key KEY"
        parsing succeed because --key could only match --key-name,
        --key_name which are current/deprecated forms of the same option.
        '''
        option_tuples = (super(UcloudClientArgumentParser, self)
                         ._get_option_tuples(option_string))
        if len(option_tuples) > 1:
            normalizeds = [option.replace('_', '-')
                           for action, option, value in option_tuples]
            if len(set(normalizeds)) == 1:
                return option_tuples[:1]
        return option_tuples


class UcloudHelpFormatter(argparse.HelpFormatter):
    '''
    shell help.
    '''

    def __init__(self, prog, indent_increment=2, max_help_position=32,
                 width=None):
        super(UcloudHelpFormatter, self).__init__(prog, indent_increment,
                                                  max_help_position, width)

    def start_section(self, heading):
        heading = '%s%s' % (heading[0].upper(), heading[1:])
        super(UcloudHelpFormatter, self).start_section(heading)


class UcloudShell(object):
    '''
    main shell class
    '''
    times = []

    def _append_env_args(self, parser):
        '''
        append env args to cli parser
        :param parser:
        :return:
        '''
        parser.set_defaults(ucloud_region=os.environ.get('UCLOUD_REGION'))
        parser.set_defaults(ucloud_url=os.environ.get('UCLOUD_URL'))
        parser.set_defaults(ucloud_pubkey=os.environ.get('UCLOUD_PUBKEY'))
        parser.set_defaults(ucloud_prikey=os.environ.get('UCLOUD_PRIKEY'))

    def get_base_parser(self):
        '''
        get cli parser
        :return:parser
        '''
        parser = UcloudClientArgumentParser(
            prog='ucloud',
            description=__doc__.strip(),
            epilog='See "ucloud help COMMAND" '
                   'for help on a specific command.',
            add_help=False,
            formatter_class=UcloudHelpFormatter,
        )

        parser.add_argument(
            '-h', '--help',
            action='store_true',
            help=argparse.SUPPRESS,
        )

        parser.add_argument(
            '--debug',
            default=False,
            action='store_true',
            help=("Print debugging output"))

        parser.add_argument(
            '--timing',
            default=False,
            action='store_true',
            help=("Print call timing info"))

        parser.add_argument(
            '--ucloud_region',
            help=argparse.SUPPRESS)

        parser.add_argument(
            '--ucloud_url',
            help=argparse.SUPPRESS)

        parser.add_argument(
            '--ucloud_pubkey',
            help=argparse.SUPPRESS)

        parser.add_argument(
            '--ucloud_prikey',
            help=argparse.SUPPRESS)

        self._append_env_args(parser)

        return parser

    def setup_debugging(self, debug):
        if not debug:
            return

        streamformat = "%(levelname)s (%(module)s:%(lineno)d) %(message)s"
        # Set up the root logger to debug so that the submodules can
        # print debug messages
        logging.basicConfig(level=logging.DEBUG,
                            format=streamformat)

    @shell_utils.arg(
        'command',
        metavar='<subcommand>',
        nargs='?',
        help='Display help for <subcommand>')
    def do_help(self, args):
        """
        Display help about this program or one of its subcommands.
        """
        if args.command:
            if args.command in self.subcommands:
                self.subcommands[args.command].print_help()
            else:
                raise uexceptions.CommandError(("'%s' is not a valid "
                                                "subcommand") % args.command)
        else:
            self.parser.print_help()

    def do_bash_completion(self, _args):
        """
        Prints all of the commands and options to stdout so that the
        ucloud.bash_completion script doesn't have to hard code them.
        """
        commands = set()
        options = set()
        for sc_str, sc in self.subcommands.items():
            commands.add(sc_str)
            for option in sc._optionals._option_string_actions.keys():
                options.add(option)

        commands.remove('bash-completion')
        commands.remove('bash_completion')
        print(' '.join(commands | options))

    def _find_actions(self, subparsers, actions_module):
        for attr in (a for a in dir(actions_module) if a.startswith('do_')):
            # I prefer to be hyphen-separated instead of underscores.
            command = attr[3:].replace('_', '-')
            callback = getattr(actions_module, attr)
            desc = callback.__doc__ or ''
            action_help = desc.strip()
            arguments = getattr(callback, 'arguments', [])

            subparser = subparsers.add_parser(
                command,
                help=action_help,
                description=desc,
                add_help=False,
                formatter_class=UcloudHelpFormatter)
            subparser.add_argument(
                '-h', '--help',
                action='help',
                help=argparse.SUPPRESS,
            )
            self.subcommands[command] = subparser
            for (args, kwargs) in arguments:
                subparser.add_argument(*args, **kwargs)
            subparser.set_defaults(func=callback)

    def _add_bash_completion_subparser(self, subparsers):
        subparser = subparsers.add_parser(
            'bash_completion',
            add_help=False,
            formatter_class=UcloudHelpFormatter
        )
        self.subcommands['bash_completion'] = subparser
        subparser.set_defaults(func=self.do_bash_completion)

    def get_subcommand_parser(self):
        parser = self.get_base_parser()

        self.subcommands = {}
        subparsers = parser.add_subparsers(metavar='<subcommand>')

        actions_module = shell_action

        self._find_actions(subparsers, actions_module)
        self._find_actions(subparsers, self)

        self._add_bash_completion_subparser(subparsers)

        return parser

    def main(self, argv):
        '''

        :param argv:
        :return:
        '''
        parser = self.get_base_parser()
        (options, args) = parser.parse_known_args(argv)
        self.setup_debugging(options.debug)

        subcommand_parser = self.get_subcommand_parser()
        self.parser = subcommand_parser

        if options.help or not argv:
            subcommand_parser.print_help()
            return 0

        args = subcommand_parser.parse_args(argv)

        if args.func == self.do_help:
            self.do_help(args)
            return 0
        elif args.func == self.do_bash_completion:
            self.do_bash_completion(args)
            return 0

        ucloud_region = args.ucloud_region
        ucloud_url = args.ucloud_url
        ucloud_pubkey = args.ucloud_pubkey
        ucloud_prikey = args.ucloud_prikey

        if not ucloud_region:
            raise uexceptions.CommandError("You must provide region "
                                           "name via --ucloud_region "
                                           "or env[UCLOUD_REGION].")

        if not ucloud_url:
            raise uexceptions.CommandError("You must provide url via "
                                           "--ucloud_url or "
                                           "env[UCLOUD_URL].")

        if not ucloud_pubkey:
            raise uexceptions.CommandError("You must provide public "
                                           "key via --ucloud_pubkey "
                                           "or env[UCLOUD_PUBKEY].")

        if not ucloud_prikey:
            raise uexceptions.CommandError("You must provide private "
                                           "key via --ucloud_prikey "
                                           "or env[UCLOUD_PRIKEY].")
        self.cs = client.Client(ucloud_url, ucloud_pubkey, ucloud_prikey,
                                debug=options.debug, timing=args.timing)

        args.func(self.cs, args)

        if args.timing:
            self._dump_timings(self.times + self.cs.get_timings())

    def _dump_timings(self, timing):
        results = [{'url': url, 'seconds': end - start} for url, start, end
                   in timing]
        total = 0.0
        for tyme in results:
            total += tyme.get('seconds')
        results.append({"Total": total})
        # if command contain more than one http request, we can type trace of
        # each request with time info.
        # shell_utils.print_list(results,["url","seconds"], sortby_index=None)

        # if command only contain one http request, type the total seconds.
        print("\nTiming>>>>\nThis Command Spent %s Seconds to Finish the HTTP "
              "request.\n" % total)


def main():
    try:
        argv = [a for a in sys.argv[1:]]
        UcloudShell().main(argv)

    except Exception as e:
        logger.debug(e, exc_info=1)
        details = {'name': encodeutils.safe_encode(e.__class__.__name__),
                   'msg': six.text_type(e)}
        print("ERROR (%(name)s): %(msg)s" % details, file=sys.stderr)
        '''
        details = {'name': encodeutils.safe_encode(e.__class__.__name__),
                   'msg': encodeutils.safe_encode(six.text_type(e))}
        print("ERROR (%(name)s): %(msg)s" % details,
              file=sys.stderr)
              '''
        sys.exit(1)
    except KeyboardInterrupt as e:
        print("... terminating nova client", file=sys.stderr)
        sys.exit(130)


if __name__ == "__main__":
    main()
