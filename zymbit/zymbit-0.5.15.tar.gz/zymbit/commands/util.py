import os
import pkgutil

from importlib import import_module

COMMANDS_DIR, UTIL_NAME = os.path.split(__file__)


def filter_parser_args(args, filter_none=True):
    parser_args = dict([(k, getattr(args, k)) for k in dir(args) if not k.startswith('_')])
    parser_args.pop('action')
    parser_args.pop('config', None)
    parser_args.pop('logfile')
    parser_args.pop('loglevel')

    if filter_none:
        keys = parser_args.keys()
        for key in keys:
            if parser_args[key] is None:
                parser_args.pop(key)

    return parser_args


def get_classes(package, subclass):
    """
    Generator that finds all classes of the given subclass

    :param package: an imported python package; e.g. import zymbit.commands
    :param subclass: subclass to search for in modules
    :return: generator
    """
    for module_path in get_modules(package):
        module = import_module(module_path)

        for name in dir(module):
            item = getattr(module, name)
            if item == subclass:
                continue

            try:
                if issubclass(item, subclass):
                    yield item
            except TypeError:
                pass


def get_modules(package):
    """
    find all 
    :param package: an imported python package; e.g. import zymbit.commands
    :return: list[string] - module paths
    """
    package_name = package.__name__
    path = package.__path__[0]
    modules = ['{}.{}'.format(package_name, name) for _, name, _ in pkgutil.iter_modules([path])]

    return modules
