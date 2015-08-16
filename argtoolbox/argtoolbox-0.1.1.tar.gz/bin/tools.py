#! /usr/bin/env python2
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK

from __future__ import unicode_literals

import sys
import locale
import codecs

from argtoolbox import DefaultCommand
from argtoolbox import BasicProgram
# pylint: disable-msg=W0611
from argtoolbox import SimpleSection
# pylint: disable-msg=W0611
from argtoolbox import Element

# if you want to debug argcomplete completion,
# you just need to export _ARC_DEBUG=True

sys.stdout = codecs.getwriter(locale.getpreferredencoding())(sys.stdout)
# -----------------------------------------------------------------------------
# pylint: disable-msg=R0903
class RenammeCommand(DefaultCommand):
    """Renamme command"""

    def __call__(self, args):
        super(RenammeCommand, self).__call__(args)
        print "New generated command : renamme"


class ToolsProgram(BasicProgram):
    """Main program."""

    def add_config_options(self):
        super(ToolsProgram, self).add_config_options()

        # To be removed if useless : samples
        # sample_section = self.config.add_section(SimpleSection("sample_section"))
        # sample_section.add_element(Element('server_name'))

    def add_commands(self):
        super(ToolsProgram, self).add_commands()

        # To be removed if useless : samples
        # self.parser.add_argument(
        #     '--server-name',
        #     **self.config.sample_section.server_name.get_arg_parse_arguments())

        subparsers = self.parser.add_subparsers()
        parser_tmp = subparsers.add_parser(
            'renamme',
            help="Description of renamme")
        parser_tmp.set_defaults(__func__=RenammeCommand(self.config))


PROG = ToolsProgram(
        "tools",
        desc="Description of program tools.")
if __name__ == "__main__":
    PROG()
