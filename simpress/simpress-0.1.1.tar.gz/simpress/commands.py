import argparse
import os
import shutil

import simpress.logger
from simpress import builder, web


def build_parser():
    parser = argparse.ArgumentParser(description='simpress bootstrap script')
    subparsers = parser.add_subparsers(help='sub-command help')

    publish_parser = subparsers.add_parser('publish',
                                           help='Publish static HTML files')
    publish_parser.set_defaults(func='publish')

    preview_parser = subparsers.add_parser('preview', help='Preview on web')
    preview_parser.add_argument('-p', '--port', type=int, default=3776)
    preview_parser.set_defaults(func='preview')
    return parser


def execute():
    simpress.logger.setup()
    parser = build_parser()
    args = parser.parse_args()
    if 'func' not in args:
        parser.error('please specify subcommand')
    globals().get(args.func)(args)


def preview(args):
    web.create_app().run(host='0.0.0.0', port=args.port)


def publish(args):
    builder.build()


def init():
    simpress.logger.setup()
    logger = simpress.logger.logger()

    parser = argparse.ArgumentParser()
    parser.add_argument('target_dir')
    args = parser.parse_args()

    if os.path.exists(args.target_dir):
        parser.error('Target directory is already exists. '
                     'Specify the new one.')

    base_dir = os.path.dirname(os.path.dirname(__file__))

    logger.info('build theme')
    shutil.copytree(
        os.path.join(base_dir, 'themes', 'default'),
        args.target_dir)

    logger.info('prepare bootstrap script')
    shutil.copy(
        os.path.join(base_dir, 'press.py'),
        args.target_dir)

    logger.info('prepare index.md')
    with open(os.path.join(args.target_dir, 'index.md'), 'w') as f:
        f.write('# index\n\nput your contents. enjoy!\n')

    logger.info('*** setup completed! ***')
    logger.info('')

    logger.info('move to "%s" and run "./press.py preview" to '
                'start Simpress preview server' % args.target_dir)
