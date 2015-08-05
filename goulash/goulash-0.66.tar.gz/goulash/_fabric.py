""" goulash._fabric

    Collection of commonly used utilities built on top of fabric
"""

from fabric import api


class MissingSystemCommand(RuntimeError):
    pass


def qlocal(*args, **kargs):
    with api.quiet():
        return api.local(*args, **kargs)
quiet_local = qlocal


def has_bin(name):
    """ answer whether a given system command
        is available on the path.  posix only """
    result = qlocal('which "{0}"'.format(name))
    return result.succeeded


def require_bin(name, msg=None):
    """ require that a given system command
        is available on the path.  posix only.
        on error, raises MissingSystemCommand
        with the supplied message """
    if not has_bin(name):
        msg = msg or "{0} is required".format(name)
        raise MissingSystemCommand(msg)
