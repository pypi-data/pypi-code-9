
"""this module defined for processing the command line

"""

from __future__ import print_function
import sys
from check_config import check_config
from generate_config import generate_config
from run_program import run_program

__support_commands_callback = {"run-program": run_program, "generate-config": generate_config,
                               'check-config': check_config}


def command_help(args):
    """define the help func for tips.
    :param args:
    :return:
    """
    if not args:
        print('Usage: tingyun-admin [command] [options]')
        print("Commands : ")

        for cmd in __support_commands_callback:
            print("    ", cmd)
    else:
        cmd = args[0]
        if cmd not in __support_commands_callback.keys():
            print("Unknown command '%s'." % cmd, end='')
            print("Type in 'tingyun-admin help' for usage.")
        else:
            cmd = __support_commands_callback[cmd]
            print('Usage: tingyun-admin %s %s' % (cmd.name, cmd.options))
            print(cmd.description)


def main():
    """
    :return:
    """
    cmd = 'help'
    if len(sys.argv) > 1:
        cmd = sys.argv[1]

    if cmd != 'help' and cmd not in __support_commands_callback:
        print("Unknown command '%s'." % cmd, end='')
        print("Type 'tingyun-admin help' for usage.")
        sys.exit(1)

    callback = __support_commands_callback.get(cmd, command_help)
    callback(sys.argv[2:])

if __name__ == '__main__':
    main()
