# -*- coding: utf-8 -*-
import os
from importlib import import_module


def available():
    mods = {}
    for path in os.listdir(os.path.dirname(__file__)):
        if not path.endswith('.py') or path == '__init__.py':
            continue
        modname = path[:-3]
        try:
            mods[modname] = import_module('{}.{}'.format(__package__, modname))
        except ImportError:
            pass
    return mods


def summary():
    '''Returns a dict of name:description for available backends'''
    backends = {}
    for name, mod in available().items():
        backends[name] = getattr(mod, 'description', 'No desciption')
    return backends


def help(backends):
    '''Prints help text for each named backend'''
    for name, mod in available().items():
        if name not in backends:
            continue
        print('-' * 79)
        print('Backend: {}'.format(name))
        print('-' * 79)
        print(mod.__doc__)


def context(backend_spec):
    '''
    Parse backend name and arguments, call the backend, and return
    the resulting context. Spec has the form backend:arg=val[,arg=val].
    Throws ImportError if the given backend does not exist.
    '''
    tokens = backend_spec.split(':')
    backend = import_module(
        '{}.{}'.format(__package__, tokens[0])
    )
    kwargs = {}
    if len(tokens) > 1:
        kwargs = dict(arg.split('=') for arg in tokens[1].split(','))

    return backend.context(**kwargs)
