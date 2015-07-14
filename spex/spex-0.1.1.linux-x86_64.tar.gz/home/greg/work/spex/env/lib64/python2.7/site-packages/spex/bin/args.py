import os
import argparse

from ..args import add_parser_options as _add_application_options  # noqa


def create_parser():
    """Create the parser for the spex tool"""
    parser = argparse.ArgumentParser(description="spex builds a PEX (Python Executable) that "
                                                 "is optimised for running spark applications")

    parser.add_argument('-v',
                        dest='verbosity',
                        default=0,
                        action='count',
                        help='Turn on logging verbosity, may be specified multiple times')

    parser.add_argument('-r', '--requirement',
                        dest='requirement_files',
                        default=[],
                        action='append',
                        type=str,
                        help='Add requirements from the given file. This option can be used multiple times')

    parser.add_argument('spex_name',
                        help='The name of the spex application')

    parser.add_argument('reqs',
                        metavar='REQ',
                        default=[],
                        nargs='*',
                        help='The requirements for this spex')

    grp = parser.add_argument_group('SPEX distribution options',
                                    description='Tailor how full distributions are built')

    grp.add_argument('--distro',
                     dest='build_distro',
                     default=False,
                     action='store_true',
                     help='Build a complete distribution, including spark and none python artifacts')

    grp.add_argument('--no-distro',
                     dest='build_distro',
                     default=False,
                     action='store_false',
                     help='Do not build a full distribution, only build the application spex file')

    grp = parser.add_argument_group('SPEX application options',
                                    description='Tailor the default options used for spex application bundles')
    grp.prog = parser.prog
    _add_application_options(grp)

    grp = parser.add_argument_group('Resolver Options',
                                    description='Tailor how to find, resolve and translate the '
                                                'packages put into the PEX environment')

    grp.add_argument('--pypi',
                     dest='use_pypi',
                     default=True,
                     action='store_true',
                     help='Use pypi to resolve dependencies')

    grp.add_argument('--no-pypi',
                     dest='use_pypi',
                     action='store_false',
                     help='Do not use pypi to resolve dependencies')

    grp.add_argument('--no-index',
                     dest='use_pypi',
                     action='store_false',
                     help='Do not use pypi to resolve dependencies')

    grp.add_argument('-f', '--find-links', '--repo',
                     dest='repos',
                     default=[],
                     action='append',
                     help='Additional repository path (directory or URL) to look for requirements')

    grp.add_argument('-i', '--index', '--index-url',
                     dest='indicies',
                     default=[],
                     action='append',
                     help='Additional cheeseshop indices to use to satisfy requirements')

    grp.add_argument('--disable-cache',
                     dest='disable_cache',
                     action='store_true',
                     help='Disable caching in the spex tool entirely')

    grp.add_argument('--cache-dir',
                     dest='cache_dir',
                     default=os.path.expanduser(os.path.join('.pex', 'build')),
                     help='The local cache directory to use for speeding up requirement lookups')

    grp.add_argument('--cache-ttl',
                     default=3600,
                     dest='cache_ttl',
                     type=float,
                     help='The cache TTL to use for inexact requirement specification')

    grp.add_argument('--wheel',
                     dest='use_wheel',
                     default=True,
                     action='store_true',
                     help='Use wheel distributions')

    grp.add_argument('--no-wheel', '--no-use-wheel',
                     dest='use_wheel',
                     action='store_false',
                     help='Do not use wheel distributions')

    grp.add_argument('--build',
                     dest='build_source',
                     default=True,
                     action='store_true',
                     help='Allow building distributions from source')

    grp.add_argument('--no-build',
                     dest='build_source',
                     action='store_false',
                     help='Do not Allow building distributions from source')

    grp = parser.add_argument_group('PEX environment options',
                                    description='Tailor the interpreter and platform targets for the PEX environment')

    grp.add_argument('--python',
                     dest='python',
                     default=None,
                     type=str,
                     help='The Python interpreter to use to build the pex. Either specify an explicit path to an '
                          'interpreter, or specify a binary accessible on $PATH. Default: Use current interpreter.')

    grp.add_argument('--python-shebang',
                     dest='python_shebang',
                     default=None,
                     type=str,
                     help='The exact shebang (#!...) line to add at the top of the PEX file minus the #!. '
                          'This overrides the default behavior, which picks an environment python interpreter '
                          'compatible with the one used to build the PEX file.')

    grp.add_argument('--platform',
                     dest='platform',
                     default='linux-x86_64',
                     type=str,
                     help='The platform for which to build the PEX.')

    grp.add_argument('--interpreter-cache-dir',
                     dest='interpreter_cache_dir',
                     default=os.path.expanduser(os.path.join('.pex', 'interpreters')),
                     help='The interpreter cache to use for keeping track of interpreter dependencies for the pex tool')

    return parser
