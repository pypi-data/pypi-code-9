import argparse
from ohh import __version__

actions = ['start', 'stop', 'login', 'status', 'setup_shell']


def make_parser():
    parser = argparse.ArgumentParser(description='ohh CLI')
    parser.add_argument('--basedir',
                        metavar='BASE_DIR',
                        type=str,
                        default='~/.ohh',
                        help='directory containing ohh data')
    parser.add_argument('--version',
                        action='version',
                        version='%(prog)s {version}'.format(version=__version__))

    subparsers = parser.add_subparsers(help='commands', dest='action')

    start_parser = subparsers.add_parser('start', help='start ohh')
    start_parser.add_argument('--foreground',
                              action='store_true',
                              help='runs the program in foreground')
    start_parser.add_argument('--office',
                              action='store_const',
                              const='office',
                              default='computer',
                              dest='session_type',
                              help='starts office session')

    stop_parser = subparsers.add_parser('stop', help='stop ohh')
    stop_parser.add_argument('--office',
                             action='store_const',
                             const='office',
                             default='computer',
                             dest='session_type',
                             help='stop office session')

    subparsers.add_parser('status', help='shows ohh status')
    subparsers.add_parser('login', help='login to the server')
    subparsers.add_parser('setup_shell', help='setup shell completion')

    return parser


def parse():
    parser = make_parser()
    return parser.parse_args()
