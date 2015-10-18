import inspect
import asyncio

import irc3
import irc3.utils
from irc3 import IrcBot

class IRCClient(object):
    defaults = dict(
        nick='echobot',
        realname='echobot',
        userinfo='echobot IRC client',
    )

    events = {"JOIN": 'joined',
              "PART": 'dramaparted',
              "QUIT": 'ragequit'}

    def __init__(self, broadcast_msg):
        self.broadcast_msg = broadcast_msg

        config = self.defaults.copy()
        config.update(inspect.getmembers(self))

        self.c = IrcBot(**config)
        self.c.recv_msg = self.recv_msg
        self.c.recv_event = self.recv_event

        self.c.include('echobot.ircplugin')
        self.c.run(forever=False)

    def format_msg(self, mask, event, target, data):
        return '<{0}> {1}'.format(mask.nick, data)

    def recv_msg(self, mask, event, target, data):
        self.broadcast_msg(self.format_msg(mask, event, target, data))

    def format_event(self, mask, event, channel, data):
        fmt = '*** {0} has {1} {2}'.format(mask.nick, self.events[event], channel)
        if data:
            fmt += ' ({0})'.format(data)
        return fmt

    def recv_event(self, mask, event, channel, data):
        self.broadcast_msg(self.format_event(mask, event, channel, data))

    @asyncio.coroutine
    def send_msg(self, msg):
        for channel in irc3.utils.as_list(getattr(self, 'autojoins', [])):
            self.c.privmsg(channel, msg)
