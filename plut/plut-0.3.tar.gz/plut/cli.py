#!/usr/local/bin python
import functools

from .utils import get_or_create_port
from .resource import PlutResource


def do_get(rc, name):
    print get_or_create_port(rc, name)


def do_remove(rc, name):
    try:
        del rc[name]
        print '%s was removed' % name
    except KeyError:
        raise KeyError('%s does not exist' % name)


def do_list(rc):
    for service, port in rc.iteritems():
        print service, port


def print_usage():
    print 'plut                -- list services'
    print 'plut rm <service>   -- remove service'
    print 'plut <service>      -- get port for service'
    return True


def cli(service=None, realservice=None, *args):
    rc = PlutResource()

    if service is None:
        return do_list(rc)

    if service == 'rm':
        if realservice is None:
            print_usage()
            return False
        return do_remove(rc, realservice)

    if service in ('help', '--help'):
        return print_usage()

    return do_get(rc, service)
