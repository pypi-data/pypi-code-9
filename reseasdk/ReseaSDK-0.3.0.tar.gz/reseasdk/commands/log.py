import sys
import argparse


SHORT_HELP = "print log emitted in tests"
LONG_HELP = """
Usage: reseasdk log
"""


def log(args):
    try:
        with(open('build/{}/boot.log'.format(args.target))) as f:
            print(f.read().rstrip())
    except FileNotFoundError:
        sys.exit("Resea SDK: log file not found")


def main(args_):
    parser = argparse.ArgumentParser(prog='reseasdk log',
                                     description='view the boot log')
    parser.add_argument('--target', default='test', help='the build target')
    args = parser.parse_args(args_)

    log(parser.parse_args(args_))
