"""Implementation of the standard :mod:`thread` module that spawns greenlets.

.. note::

    This module is a helper for :mod:`gevent.monkey` and is not intended to be
    used directly. For spawning greenlets in your applications, prefer
    :class:`Greenlet` class.
"""
from __future__ import absolute_import
import sys

__implements__ = ['allocate_lock',
                  'get_ident',
                  'exit',
                  'LockType',
                  'stack_size',
                  'start_new_thread',
                  '_local']

__imports__ = ['error']
if sys.version_info[0] <= 2:
    import thread as __thread__
else:
    import _thread as __thread__
    __target__ = '_thread'
    __imports__ += ['RLock',
                    'TIMEOUT_MAX',
                    'allocate',
                    'exit_thread',
                    'interrupt_main',
                    'start_new']
error = __thread__.error
from gevent.hub import getcurrent, GreenletExit
from gevent.greenlet import Greenlet
from gevent.lock import BoundedSemaphore
from gevent.local import local as _local


def get_ident(gr=None):
    if gr is None:
        return id(getcurrent())
    else:
        return id(gr)


def start_new_thread(function, args=(), kwargs={}):
    greenlet = Greenlet.spawn(function, *args, **kwargs)
    return get_ident(greenlet)


class LockType(BoundedSemaphore):
    # Change the ValueError into the appropriate thread error
    # and any other API changes we need to make to match behaviour
    _OVER_RELEASE_ERROR = __thread__.error

allocate_lock = LockType


def exit():
    raise GreenletExit


if hasattr(__thread__, 'stack_size'):
    _original_stack_size = __thread__.stack_size

    def stack_size(size=None):
        if size is None:
            return _original_stack_size()
        if size > _original_stack_size():
            return _original_stack_size(size)
        else:
            pass
            # not going to decrease stack_size, because otherwise other greenlets in this thread will suffer
else:
    __implements__.remove('stack_size')

for name in __imports__[:]:
    try:
        value = getattr(__thread__, name)
        globals()[name] = value
    except AttributeError:
        __imports__.remove(name)

__all__ = __implements__ + __imports__
__all__.remove('_local')

# XXX interrupt_main
# XXX _count()
