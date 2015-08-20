# coding: utf-8

'''
    fabric_bearychat
    ~~~~~~~~~~~~~~~~

    Fabric tasks aided with bearychat.

    Tasks will use these env vars:

    - `bearychat_hook` bearychat incoming robot hook (optional).
    - `bearychat_channel` bearychat incoming channel (optional).
'''

from functools import wraps

from bearychat import Incoming
from fabric.api import env
from fabric.utils import warn, abort


def _must_get_hook(override=None, silent=True):
    if override is not None:
        return override
    if 'bearychat_hook' not in env:
        wrong = warn if silent else abort
        wrong('You must set env var `bearychat_hook` before using bearychat.')
    return env.bearychat_hook


def _get_channel(override=None):
    if override is not Incoming.DEFAULT_CHANNEL:
        return override
    return env.get('bearychat_channel', Incoming.DEFAULT_CHANNEL)


def notify(message, hook=None, channel=Incoming.DEFAULT_CHANNEL, silent=True):
    '''Send a message to bearychat.'''
    Incoming(_must_get_hook(hook, silent)) \
        .to(_get_channel(channel)) \
        .with_text(message) \
        .push()


class notify_when_finished(object):
    '''A decorator for sending notification after task executation.


            @notify_when_finished('task A is finished', 'task A is failed')
            @task
            def task_a():
                ...
    '''

    def __init__(self,
                 on_succeeded=None,
                 on_failed=None,
                 hook=None,
                 channel=Incoming.DEFAULT_CHANNEL):
        self.message_on_succeeded = on_succeeded
        self.message_on_failed = on_failed
        self.hook = hook
        self.channel = channel

    def __call__(self, task):
        @wraps(task)
        def wrapper(*args, **kwargs):
            try:
                rv = task(*args, **kwargs)

                self._build_and_send_message(
                    self.message_on_succeeded,
                    '{} is finished'.format(task.__name__)
                )

                return rv
            except Exception as e:
                self._build_and_send_message(
                    self.message_on_failed,
                    repr(e)
                )
                raise
        return wrapper

    def _build_and_send_message(self, message, default):
        if callable(message):
            message = message()
        if message is None:
            message = default
        notify(message, self.hook, self.channel)
