# -*- coding: utf-8 -*-
'''
Render templates based on data from various sources, such as environment
variables and AWS metadata. Every file in the template directory is rendered
to the equivalent path under the target root. For example:

    templates/etc/foo/bar.conf -> ${TARGET_ROOT}/etc/foo/bar.conf
    templates/var/lib/baz.conf -> ${TARGET_ROOT}/var/lib/baz.conf
'''
import os
from argparse import (
    ArgumentParser,
    RawTextHelpFormatter,
)
import logging
from pprint import pformat
import sys
from . import template
from . import backends

log = logging.getLogger(__name__)


def handle_args(arguments=sys.argv[1:]):
    desc = __doc__
    desc += '\n\nAvailable backends:\n'
    for backend_name, backend_desc in backends.summary().items():
        desc += '\n  {}: {}'.format(backend_name, backend_desc)

    ap = ArgumentParser(
        description=desc,
        formatter_class=RawTextHelpFormatter
    )
    ap.add_argument(
        '--backend-help', dest='backend_help', action='store_true',
        help='Print help for given backends.',
    )
    ap.add_argument(
        '--template-dir', dest='template_dir',
        default='templates', metavar='DIR',
        help='Directory containing templates.',
    )
    ap.add_argument(
        '--target-root', dest='target_root',
        default='', metavar='DIR',
        help='Root directory for rendered templates. Defaults to the current '
        'working directory.',
    )
    ap.add_argument(
        'backend', nargs='+',
        help='Datasource backends, highest priority first.',
    )
    ap.add_argument(
        '--loglevel',
        metavar='ERROR,WARNING,...'
    )
    return ap, ap.parse_args()


def main():
    ap, args = handle_args()

    if not args.loglevel:
        args.loglevel = os.environ.get('RC_LOGLEVEL') or 'ERROR'

    logging.basicConfig()
    log = logging.getLogger(os.path.basename(sys.argv[0]))
    log.setLevel(args.loglevel)

    if args.backend_help:
        backends.help(args.backend)
        exit(0)

    context = {}
    backend_errors = []
    for backend in args.backend[::-1]:
        try:
            context.update(backends.context(backend))
        except ImportError as e:
            backend_errors.append((backend, e))
    if backend_errors:
        for backend, error in backend_errors:
            log.error('Error loading backend "{}": {}'.format(backend, error))
        exit(1)
    log.debug('Template context:\n{}'.format(pformat(context)))

    try:
        template.render(args.template_dir, context, args.target_root)
    except template.RenderError as e:
        log.error('Error rendering templates: {}'.format(e))
        exit(1)

if __name__ == '__main__':
    main()
