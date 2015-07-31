"""
Lists old versions of a corrected message.

Usage
-----

.. glossary::

    /display_corrections
        **Usage:** ``/display_corrections [number]``

        This command lists the old versions of a message.

        Without argument, it will list the last corrected message if there
        is any. If you give an integer as an argument, ``/display_corrections``
        will go back gradually in the buffer to find the message matching
        that number (starting from 1, for the last corrected message).

        If you are scrolling in the buffer, Poezio will list the corrected messages
        starting from the first you can see.  (although there are some problems with
        multiline messages).


"""
from plugin import BasePlugin
import difflib
from functools import wraps
import tabs
from config import config

shim_message_fields = ('txt nick_color time str_time nickname user identifier'
                  ' highlight me old_message revisions jid ack')
ShimMessage = collections.namedtuple('ShimMessage', shim_message_fields)

def other_elems(self):
    "Helper for the repr_message function"
    acc = ['Message(']
    fields = message_fields.split()
    fields.remove('old_message')
    for field in fields:
        acc.append('%s=%s' % (field, repr(getattr(self, field))))
    return ', '.join(acc) + ', old_message='

def repr_message(self):
    """
    repr() for the Message class, for debug purposes, since the default
    repr() is recursive, so it can stack overflow given too many revisions
    of a message
    """
    init = other_elems(self)
    acc = [init]
    next_message = self.old_message
    rev = 1
    while next_message:
        acc.append(other_elems(next_message))
        next_message = next_message.old_message
        rev += 1
    acc.append('None')
    while rev:
        acc.append(')')
        rev -= 1
    return ''.join(acc)

Message.__repr__ = repr_message
Message.__str__ = repr_message



def corrections_enabled(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if config.get('group_corrections'):
            return
        return func(*args, **kwargs)
    return wrapper

class Plugin(BasePlugin):
    def init(self):
        self.api.add_event_handler('conversation_msg', self.on_message)
        self.api.add_event_handler('private_msg', self.on_message)
        self.api.add_event_handler('muc_msg', self.on_muc_message)

    @corrections_enabled
    def on_message(self, message, tab):
        pass

    @corrections_enabled
    def on_muc_message(self, message, tab):
        pass

    def command_display_corrections(self, args):
        args = shell_split(args)
        if len(args) == 1:
            try:
                nb = int(args[0])
            except:
                return self.api.run_command('/help display_corrections')
        else:
            nb = 1
        message = self.find_corrected(nb)
        if message:
            display = []
            while message:
                display.append('%s %s%s%s %s' % (message.str_time, '* ' if message.me else '', message.nickname, '' if message.me else '>', message.txt))
                message = message.old_message
            self.api.information('Older versions:\n' + '\n'.join(display[::-1]), 'Info')
        else:
            self.api.information('No corrected message found.', 'Warning')

    def cleanup(self):
        del self.config
