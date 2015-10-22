import logging
import os
import pkg_resources
import sys
from collections import namedtuple
from argparse import ArgumentParser


Plugin = namedtuple('Plugin', 'add_command_line_arguments, run_command, add_options')


def _load_plugins():
    plugins = []
    for ep in pkg_resources.iter_entry_points('cleanenv'):
        module = ep.load()
        plugins.append((ep.name, module))
    return plugins


def _get_plugin(module):
    add_command_line_arguments = []
    add_options = []

    try:
        run_command = module.run_command
    except AttributeError:
        return

    try:
        add_options.append(module.add_options)
    except AttributeError:
        pass

    need_environment = getattr(module, 'NEEDS_ENVIRONMENT', False)
    if need_environment:
        add_command_line_arguments.append(add_environment_argument)
        add_options.append(add_environment_options)

    try:
        add_command_line_arguments.append(module.add_command_line_arguments)
    except AttributeError:
        pass

    return Plugin(add_command_line_arguments, run_command, add_options)


def get_environment():
    environ = {}
    if os.environ.get('CLEAN_ENV'):
        environ['CLEAN_ENV'] = os.environ['CLEAN_ENV']
    return environ


def add_environment_argument(parser, environ):
    """For commands that requires an environment.
    """
    default = None
    if environ.get('CLEAN_ENV'):
        default = environ['CLEAN_ENV']
    else:
        realpath = os.path.dirname(os.path.realpath(sys.argv[0]))
        if realpath.split(os.path.sep)[-2:] == ['.env', 'bin']:
            if os.path.join(realpath, '..', '..', 'cleanenv.conf'):
                default_rel = os.path.join(realpath, '..', '..')
                default = os.path.abspath(default_rel)

    if default:
        help_default = ' Default: %s' % default
    else:
        help_default = ''

    parser.add_argument('-e',
        dest='environment_path',
        default=default,
        required=not bool(default),
        help='Path to cleanenv environment%s' % help_default)


def standalone_command_main(module):
    plugin = _get_plugin(module)
    parser = ArgumentParser()
    for callback in plugin.add_command_line_arguments:
        callback(parser, get_environment())
    options = parser.parse_args()
    for callback in plugin.add_options:
        callback(options)
    setup_logging()
    plugin.run_command(options)


def add_environment_options(options):
    """For standalone commands.
    """
    home_dir             = options.environment_path
    options.bin_dir      = os.path.join(home_dir, 'bin')
    options.config_file  = os.path.join(home_dir, 'cleanenv.conf')
    options.counter_file = os.path.join(home_dir, 'usage.counter')


def _version():
    try:
        return pkg_resources.get_distribution('cleanenv_inside').version
    except pkg_resources.DistributionNotFound:
        return pkg_resources.get_distribution('cleanenv').version


def main():
    plugins = _load_plugins()

    parser = ArgumentParser()
    parser.add_argument('-V', '--version', action='version', version=_version())
    subparsers = parser.add_subparsers(dest='command')

    # add plugin commands
    commands = {}
    environ = get_environment()
    for name, module in plugins:
        plugin = _get_plugin(module)
        if not plugin:
            continue

        subparser = subparsers.add_parser(name)
        for callback in plugin.add_command_line_arguments:
            callback(subparser, environ)

        commands[name] = plugin

    options = parser.parse_args()
    com = commands[options.command]

    for callback in com.add_options:
        callback(options)

    setup_logging()
    com.run_command(options)


def setup_logging():
    logging.basicConfig(level=logging.INFO)


if __name__ == '__main__':
    main()

