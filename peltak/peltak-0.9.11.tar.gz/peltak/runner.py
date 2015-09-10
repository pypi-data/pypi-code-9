#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import sys
import os
import os.path
import readline
import logging
import copy
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from peltak.config import ACTIONS_DIRS
from peltak.core import cstr
from peltak.system import forms
from peltak.config import LOG_FILENAME, MR_TEMPLATE_PATH
from peltak.actions import actions
from peltak.system.appcontext import AppContext
from peltak.common.utils import fetch_template


if not os.path.exists(os.path.dirname(LOG_FILENAME)):
    os.makedirs(os.path.dirname(LOG_FILENAME))
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)


class ActionError(RuntimeError):
    pass



def mkcmdline():
    alist = sorted(actions.iter(), key=lambda x: x.name)
    cmdline = ArgumentParser(
        usage=cstr("^33%(prog)s^0 ^32action^0 [options] [action args]"),
        formatter_class = RawDescriptionHelpFormatter,
        description=cstr('\n'.join([
            "^33peltak^0 is a command line utility to improve your daily workflow.",
            "The main focus so far is making a gitlab merge request"
            " management easier.",
            "",
            "  List all available actions along with a short description",
            "  ^1$ %(prog)s list-actions^0",
            "",
            "  More detailed help about a particular action",
            "  ^1$ %(prog)s <command> --help^0",
            "",
            "Available actions:",
            "  " + '\n  '.join(cstr('^32{}^0').format(a.name) for a in alist)
        ]))
    )

    return cmdline


def preparse_cmdline():
    """ Extract action from the command line.

    Only the first argument can be an action. If it doesn't start with '-' it
    is considered one. Otherwise action = None will be returned along with the
    whole command line. If the action is found, this funtion will return
    the action name and the command line with action arg removed.
    """
    args = sys.argv[1:]
    action = None
    if len(args) > 0 and not args[0].startswith('-'):
        action = args[0]
        args = args[1:]
    return action, args


def parse_cmdline(cmdline):
    """ Parse command line and return action and args.

    This function assumes actions.discover() was already called. It will
    read the action name from the command line and find the matching action.
    If the action cannot be found, ``ActionError`` will be raised.

    It will collect all the command line arguments from the action and parse
    the command line using that specification.

    """
    aname, args = preparse_cmdline()
    action = actions.find(aname)

    if action is not None:
        if 'cmdline' in action.meta:
            for arg in action.meta.cmdline:
                kwargs = copy.copy(arg)
                kwargs.pop('args')
                cmdline.add_argument(*arg['args'], **kwargs)

        cmdline.description = ""
        cmdline.epilog = action.meta.get('desc', '')

    cl = cmdline.parse_args(args)
    if action is None:
        raise ActionError("'{}' action not found".format(aname))

    return action, cl


def main():
    actions.discover(ACTIONS_DIRS)
    readline.parse_and_bind('tab: complete')

    cl = mkcmdline()
    try:
        action, cl = parse_cmdline(cl)
        app = AppContext(cl)

        action.run(app)
    except ActionError as ex:
        print("\033[31m{}\033[0m".format(str(ex)))
        cl.print_help()


if __name__ == '__main__':
    main()

