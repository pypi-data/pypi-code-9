from __future__ import print_function
import os
import pkg_resources
import shutil
import sys

import six
import virtualenv
try:
    import subprocess32 as subprocess
except ImportError:
    import subprocess

from ..cleanenv_inside.commands import link
from ..cleanenv_inside.config import Config
from ..cleanenv_inside.user import getlogin, getuid


def add_command_line_arguments(parser, _environ):
    username = getlogin()
    uid      = getuid()
    user     = '%d:%s' % (uid, username)

    parser.add_argument('-b', '--base-image',
        help='Base docker image.',
        dest='base_image')
    parser.add_argument('-c', '--config',
        help='Use a configuration file to setup an environment',
        metavar='CONFIG_FILE',
        dest='config_file')
    parser.add_argument('--on-activate',
        help='Execute PROGRAM (inside the container) on environment activation',
        action='append',
        default=[],
        metavar='PROGRAM',
        dest='on_activate')
#    parser.add_argument('--on-deactivate',
#        help='Execute PROGRAM (inside the container) on environment deactivation',
#        action='append',
#        default=[],
#        metavar='PROGRAM',
#        dest='on_deactivate')
#    parser.add_argument('--on-destroy',
#        help='Execute PROGRAM (inside the container) on environment destruction.',
#        action='append',
#        default=[],
#        metavar='PROGRAM',
#        dest='on_destroy')
    parser.add_argument('--sudo',
        help="Set sudo for --user without password",
        action='store_true',
        dest='sudo')
    parser.add_argument('-u', '--user',
        help='Set the user inside the container. Defaults to "%s". Format is ' \
            '"[system:][<uid>:][<username>]"' % user,
        metavar='USER',
        default=user,
        dest='user')
    parser.add_argument('--link',
        help='Link a program inside the container to the outside. Format is [<host-link-name>:]<container-path>',
        action='append',
        default=[],
        metavar='PROGRAM',
        dest='link')
    parser.add_argument('-d', '--directory',
        help='Mount a directory into the container. Format is ' \
            '"<host-path>:<container-path>[:rw]". By default, /r is mounted ' \
            'read-only.',
        action='append',
        default=[],
        metavar='DIR',
        dest='directory')
    parser.add_argument('-p', '--persistent',
        help='Keep the container running, even on environment deactivation.',
        action='store_true',
        dest='persistent')
    parser.add_argument('--generate-config-file',
        help='Generate a configuration file for later usage with the "-c <config-path>" option.',
        action='store_true',
        dest='generate_config')

    parser.add_argument('dest_dir',
        help='Path where to install the environment',
        metavar='DEST_DIR')


def _destroy(home_dir):
    if not os.path.exists(home_dir):
        return

    executable = os.path.join(home_dir, 'bin', 'cleanenv')

    if not os.path.exists(executable):
        print("%s does not exists. Aborting." % executable, file=sys.stderr)
        sys.exit(1)

    cmd = [executable, 'destroy']

    subprocess.check_call(cmd)


def run_command(options):
    dest_dir = options.dest_dir
    bin_dir  = os.path.join(dest_dir, 'bin')
    venv_dir = os.path.join(dest_dir, '.env')
    resource_dir = _pkg_resource_dir()

    if options.generate_config:
        config_file = dest_dir
        config = _generate_config_file(options, config_file)
        config.write()
        return

    # check configuration before doing anything else
    _generate_config_file(options, None).check()

    # clear existing if exist
    _destroy(dest_dir)

    print("Creating %s" % dest_dir)
    virtualenv.create_environment(
        venv_dir, site_packages=False, clear=True, never_download=True)

    _install_cleanenv_inside(venv_dir)

    # install common files
    os.mkdir(bin_dir)
    shutil.copy(os.path.join(resource_dir, 'activate'), bin_dir)

    # create symlinks
    for basename in ['cleanenv', 'inenv']:
        venv_bin_dir = os.path.join('..', '.env', 'bin', basename)
        os.symlink(venv_bin_dir, os.path.join(bin_dir, basename))

    # write config file
    config_file = os.path.join(dest_dir, 'cleanenv.conf')
    config = _generate_config_file(options, config_file)
    config.write()

    link.install_program_links(bin_dir, config)


def _pkg_resource_dir():
    dist = pkg_resources.resource_filename('cleanenv', 'distribution')
    if not os.path.isdir(dist):
        raise IOError('%s is not a directory' % (dist, ))

    return dist


def _pkg_resource_dir_cleanenv():
    dist = pkg_resources.resource_filename('cleanenv', '')
    if not os.path.isdir(dist):
        raise IOError('%s is not a directory' % (dist, ))

    return dist


def _install_cleanenv_inside(dest_dir):
    to_install = ['docker-py', 'configobj']
    if six.PY2:
        to_install += ['subprocess32']

        if sys.version_info[1] <= 6:
            to_install += ['argparse']
    print("Installing %s" % ', '.join(to_install))
    search_dir = 'file://' + _pkg_resource_dir()

    pip_executable = os.path.join(dest_dir, 'bin', 'pip')
    cmd = [
        pip_executable,
        'install',
        '--ignore-installed',
        '--no-index',
        '-f', search_dir] + to_install

    subprocess.check_call(cmd, stdout=subprocess.PIPE)

    print("Installing cleanenv_inside")
    search_dir = _pkg_resource_dir_cleanenv()
    cmd = [
        pip_executable,
        'install',
        '--no-deps',
        '--no-index',
        search_dir]
    subprocess.check_call(cmd, stdout=subprocess.PIPE)


def _generate_config_file(options, filepath):
    config = Config(filepath, file_error=False, validate=False)

    if options.config_file:
        from_config = Config(options.config_file)
        config.update(from_config)

    if options.user:
        config['global']['user'] = options.user
    if options.sudo:
        config['global']['sudo'] = True
    if options.persistent:
        config['global']['persistent'] = True
    if options.base_image:
        config['global']['base'] = options.base_image
    for program in options.on_activate:
        config['global']['on_activate'].append(program)
    for directory in options.directory:
        splitted = directory.split(':')
        if len(splitted) not in (2, 3):
            raise ValueError('--directory=%s is in wrong format.' % directory)
        dest, source = splitted[:2]
        if len(splitted) == 3:
            flag = splitted[2]
        else:
            flag = 'ro'
        source = source + ':' + flag
        if dest in config['directory']:
            raise ValueError('--directory=%s appears more than once.' % directory)
        config['directory'][dest] = source
    for value in options.link:
        splitted = value.split(':', 1)
        if len(splitted) == 2:
            dest, source = splitted
        else:
            dest = os.path.basename(value)
            source = value
        config['link'][dest] = source

    config.check()

    return config

