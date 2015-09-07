import subprocess
import os

from . import *
from ..cache import format

_FILE_PREFIX = 'amazonclouddrive:'
null = open(os.devnull, 'wb')


class ClementinePlugin(Plugin):
    """Adds node to clementine playlist. Creates instance if none is running."""
    MIN_VERSION = '0.3.0a6'

    @classmethod
    def attach(cls, subparsers: argparse.ArgumentParser, log: list, **kwargs):
        try:
            subprocess.call(['clementine', '--version'], stderr=null, stdout=null)
        except FileNotFoundError:
            log.append('Clementine executable not found.')
            return

        p = subparsers.add_parser('clementine', add_help=False, description='foo')
        p.add_argument('--replace', dest='mode', action='store_const',
                       const='--load', default='--append',
                       help='replaces current playlist [default: append]')
        p.add_argument('--shuffle', action='store_true')
        p.add_argument('--log', '-l', action='store_true')
        p.add_argument('node', help='')
        p.set_defaults(func=cls.action)

        log.append(cls.__name__ + ' attached.')

    @staticmethod
    def action(args: argparse.Namespace) -> int:
        import logging
        import mimetypes
        import random

        logger = logging.getLogger(__name__)

        node = args.cache().get_node(args.node)
        if not node:
            logger.critical('Invalid node ID.')
            return 1

        bunches = []
        if node.is_file():
            bunches = [args.cache().Bunch(node=node)]
        elif node.is_folder():
            bunches = args.cache().list_children(node.id, recursive=True)

        acc = []
        for bunch in bunches:
            node = bunch.node
            if node.is_file():
                mt = mimetypes.guess_type(node.name)[0]
                if not mt:
                    continue
                mt = mt.split('/')[0]
                if mt == 'audio':
                    acc.append(bunch)
        node_ids = [id for id in format.IDFormatter(acc)]

        logger.info('%s audio files to add.' % len(node_ids))
        if len(node_ids) == 0:
            logger.warning('No nodes to add.')
            return 1

        if args.shuffle:
            random.shuffle(node_ids)

        p_args = ['clementine', args.mode]
        p_args.extend([_FILE_PREFIX + l for l in node_ids])

        # this should launch a detached process
        subprocess.Popen(p_args, stderr=null if not args.log else None,
                         stdout=null if not args.log else None)
