__author__ = 'Sinisa'

import docopt
import sbg_cli
from sbg_cli import __version__, disable_warnings
from sbg_cli.command import get_utils, sbg_usage


BASECOMMAND = 'sbg'


USAGE = '''
    Seven Bridges Genomics Utilities.

    Usage:
{usage}
    '''


def main():
    disable_warnings()
    utils = get_utils(sbg_cli, BASECOMMAND)
    usage = USAGE.format(usage=sbg_usage(utils))
    try:
        args = docopt.docopt(usage, version=__version__)
    except Exception:
        print(usage)
    for u in utils:
        for cmd in u.commands:
            if args[cmd]:
                u(cmd, **args)


if __name__=='__main__':
    main()
