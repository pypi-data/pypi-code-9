import datetime
import functools
import asyncio

from slixmpp import ClientXMPP

class HipchatClient(object):
    def __init__(self, broadcast_msg):
        self.broadcast_msg = broadcast_msg

        self.c = ClientXMPP(self.jabber_id, self.password)
        self.c.register_plugin('xep_0030')  # Service Discovery
        self.c.register_plugin('xep_0045')  # Multi-User Chat
        self.c.register_plugin('xep_0199')  # XMPP Ping
        self.c.register_plugin('xep_0203')  # XMPP Delayed messages
        self.c.register_plugin('xep_0249')  # XMPP direct MUC invites

        self.c.auto_authorize = True
        self.c.auto_subscribe = True

        self.c.whitespace_keepalive = True
        self.c.whitespace_keepalive_interval = 60

        self.c.add_event_handler('session_bind', self.session_start)
        self.c.add_event_handler('session_bind', self.c._start_keepalive)

        for room, _ in self.rooms:
            self.c.add_event_handler('muc::{}::message'.format(room), self.muc_message)
            self.c.add_event_handler('muc::{}::got_offline'.format(room), functools.partial(self.send_presence, 'parted'))
            self.c.add_event_handler('muc::{}::got_online'.format(room), functools.partial(self.send_presence, 'joined'))

        self.c.connect()

    def session_start(self, event):
        self.c.send_presence()
        self.c.get_roster()

        for room, password in self.rooms:
            self.c.plugin['xep_0045'].joinMUC(room, self.nickname, password=password, wait=True)

    def muc_message(self, msg):
        # yes, this is how you check to see if 'delay' is set on a message.
        # this API is dumb
        if isinstance(msg['delay']['stamp'], datetime.datetime):
            return
        if msg['from'].resource == self.nickname:
            return
        self.broadcast_msg(self.format_msg(msg))

    def format_msg(self, msg):
        return '({0}) {1}'.format(msg['from'].resource, msg['body'])

    def format_presence(self, user, status):
        return '*** {0} has {1}'.format(user, status)

    def send_presence(self, status, msg):
        self.broadcast_msg(self.format_presence(msg['from'].resource, status))

    @asyncio.coroutine
    def send_msg(self, msg):
        for room, _ in self.rooms:
            self.c.send_message(mto=room, mbody=msg, mtype='groupchat')
