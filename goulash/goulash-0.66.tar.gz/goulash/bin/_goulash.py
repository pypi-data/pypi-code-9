""" goulash.bin._goulash
"""
import os
from argparse import ArgumentParser

from peak.util.imports import lazyModule

from goulash import version

fileserver = lazyModule('goulash.fileserver')
inspect = lazyModule('goulash._inspect')
projects = lazyModule('goulash.projects')
boiler = lazyModule('goulash.bin.boiler')
from goulash.docs import docs_handler
from jinja2 import Template


def get_parser():
    """ build the default parser """
    parser = ArgumentParser()
    # parser.set_conflict_handler("resolve")
    parser.add_argument(
        "-v", '--version', default=False, dest='version',
        action='store_true',
        help=("show version information"))
    subparsers = parser.add_subparsers(help='commands')
    help_parser = subparsers.add_parser('help', help='show help info')
    help_parser.set_defaults(subcommand='help')

    bparser = subparsers.add_parser('boiler', help='boilerplate generation')
    bparser.add_argument(
        "--docs", default=False, dest='docs',
        action='store_true',
        help=("create docs boilerplate for python project"))
    bparser.add_argument(
        "--tox", default=False, dest='tox',
        action='store_true',
        help=("create tox boilerplate for python project"))
    bparser.add_argument(
        "--tests", default=False, dest='tests',
        action='store_true',
        help=("create test boilerplate for python project"))
    bparser.add_argument(
        "--pypi", default=False, dest='tests',
        action='store_true',
        help=("create pypi boilerplate for python project"))
    bparser.add_argument(
        "--project", default=False, dest='project',
        action='store_true',
        help=("create all boilerplate for python project"))
    bparser.add_argument(
        "--pkg_name", default='', dest='pkg_name',
        help=("python pkg_name"))
    bparser.add_argument(
        "--pkg", default=False, dest='pkg',
        action='store_true',
        help=("create all boilerplate for python package"))
    # bparser.add_argument(
    #    "--project", default='', dest='project',
    #    required=True,
    #    help=("project name"))
    bparser.add_argument(
        'dir', nargs='?', default=os.getcwd(),
        help=("base directory to generate boilerplate in"))
    bparser.set_defaults(subcommand='boiler')

    version_parser = subparsers.add_parser(
        'version', help='show goulash version')
    version_parser.set_defaults(subcommand='version')

    project_parser = subparsers.add_parser(
        'project', help='project based subcommands')
    project_parser.set_defaults(subcommand='project')
    project_parser.add_argument(
        '-b', default=False, action='store_true',
        dest='version_bump',
        help=("bump version for pkg_root"))
    project_parser.add_argument(
        '--pypi-publish', default=False,
        action='store_true',
        dest='pypi_publish',
        help=("refresh pypi"))

    serve_parser = subparsers.add_parser(
        'serve', help='simple threaded directory-indexing http server')
    serve_parser.set_defaults(subcommand='serve')
    serve_parser.add_argument(
        "--port", default='', dest='port',
        help=("port for http server"))
    serve_parser.add_argument(
        "-v", '--version', default=False, dest='version',
        action='store_true',
        help=("show version information"))
    serve_parser.add_argument(
        'dir', nargs='?', default=os.getcwd(),
        help=("directory to serve files from"))

    docs_parser = subparsers.add_parser(
        'docs', help='utilities for documentation')
    docs_parser.set_defaults(subcommand='docs')
    docs_parser.add_argument(
        "--boiler-plate", '-b', default=False, dest='boilerplate',
        action='store_true',
        help=("create docs boilerplate for a python project"))
    # docs_parser.add_argument(
    #    "--project", '-p', default='', dest='project',
    # help=("Specifies project name (required if $PROJECT_NAME is not set)"))
    docs_parser.add_argument(
        "--refresh", '-r',
        default=False, dest='refresh',
        action='store_true',
        help=("refresh this projects documentation"))
    docs_parser.add_argument(
        "--show", '-s',
        default=False, dest='show',
        action='store_true',
        help=("show this projects documentation"))
    docs_parser.add_argument(
        '--deploy',
        default=False,
        dest='deploy', action='store_true',
        help='like mkdocs deploy')
    docs_parser.add_argument(
        'docroot', nargs='?', default='docs',
        help=("base directory for docs"))
    docs_parser.add_argument(
        "-v", '--version', default=False, dest='version',
        action='store_true',
        help=("show version information"))
    return parser


def project_handler(args):
    if args.version_bump:
        projects.version_bump()
    elif args.pypi_publish:
        projects.pypi_publish()
    else:
        raise SystemExit("unknown project subcommand")

from goulash.boiler import boiler_handler


def entry():
    parser = get_parser()
    args = parser.parse_args()
    if args.subcommand in ['version', 'help']:
        if args.subcommand == 'version':
            print version.__version__
        if args.subcommand == 'help':
            parser.print_help()
        raise SystemExit()
    elif args.subcommand == 'project':
        project_handler(args)
    elif args.subcommand == 'serve':
        fileserver.main(args)
    elif args.subcommand == 'docs':
        docs_handler(args)
    elif args.subcommand == 'boiler':
        boiler_handler(args)
    else:
        raise SystemExit('unknown subcommand')
