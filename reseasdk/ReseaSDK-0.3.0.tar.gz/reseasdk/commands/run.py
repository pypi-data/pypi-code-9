import argparse
import hashlib
import os
import sys
import time
import threading
import watchdog
import watchdog.events
import watchdog.observers
from reseasdk.run import run_emulator
from reseasdk.helpers import info, notice, error, \
    dict_to_strdict
from reseasdk.commands.build import build


SHORT_HELP = "build and run"
LONG_HELP = """
Usage: reseasdk run
"""


def run(args):
    cs = build(args)
    defaults = cs['defaults']

    info('ReseaSDK: build finished successfully, starting the executable...')
    env = dict_to_strdict(defaults)
    cmd = [defaults['HAL_RUN'], defaults['BUILD_DIR'] + '/application']
    run_emulator(cmd, save_log='build/{}/boot.log'.format(args['target']),
                 env=env)


def main(args_):
    parser = argparse.ArgumentParser(prog='reseasdk run',
                                     description='run an executable')
    parser.add_argument('-r', action='store_true',
                        help='rebuild the executable')
    parser.add_argument('--target', default='build', help='the build target')
    parser.add_argument('--dump', action='store_true',
                        help='dump generated files for debugging')
    parser.add_argument('--no-prettify', action='store_true',
                        help="don't prettify output")
    parser.add_argument('--all-in-one', action='store_true',
                        help='embed all required applications so that'
                        'discovery() always succeed')
    parser.add_argument('--single-app', action='store_true',
                        help='no threading')
    parser.add_argument('defaults', nargs='*',
                        help='default variables (FOO=bar)')

    args = vars(parser.parse_args(args_))
    run(args)
