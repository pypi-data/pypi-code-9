import sys
import argparse

from env2config.main import build
from env2config.main import inject
from env2config.util import tags_to_dict, create_logger

USAGE = '''
USAGE:
    env2config build <service_name> <version> [<default_config_folder>=./default_configs]
    env2config inject [<default_config_folder>=./default_configs]
'''.strip()


def ensure(result):
    if result is True:
        sys.exit(0)
    else:
        sys.exit(2)

logger = create_logger()

parser = argparse.ArgumentParser(description='Inject variables into configuration files.')
cmd_parsers = parser.add_subparsers()

build_cmd = cmd_parsers.add_parser('build', help='Download default configuration files.')
inject_cmd = cmd_parsers.add_parser('inject', help='Inject variables to override configuration files.')

build_cmd.add_argument('service_name')
build_cmd.add_argument('version')
build_cmd.add_argument('default_config_folder', nargs='?', default='./default_configs')
build_cmd.add_argument('-t', '--tag', action='append')

inject_cmd.add_argument('default_config_folder', nargs='?', default='./default_configs')


def main_build(args):
    logger.debug('args: %s', args)
    tags = tags_to_dict(args.tag)
    ensure(build(args.service_name, args.version, args.default_config_folder, tags))

build_cmd.set_defaults(func=main_build)


def main_inject(args):
    logger.debug('args: %s', args)
    ensure(inject(args.default_config_folder))

inject_cmd.set_defaults(func=main_inject)

args = parser.parse_args()
args.func(args)

print(USAGE)
sys.exit(1)
