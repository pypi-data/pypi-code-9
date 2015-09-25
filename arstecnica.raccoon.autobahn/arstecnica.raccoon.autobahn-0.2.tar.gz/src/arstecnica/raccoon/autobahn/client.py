# -*- coding: utf-8 -*-
# :Progetto:  arstecnica.raccoon.autobahn -- Autobahn client
# :Creato:    ven 10 lug 2015 02:47:22 CEST
# :Autore:    Alberto Berti <alberto@metapensiero.it>
# :Licenza:   GNU General Public License version 3 or later
#

import asyncio
import logging

from autobahn.asyncio import wamp
from autobahn.asyncio.websocket import WampWebSocketClientFactory
from autobahn.wamp.types import ComponentConfig, CallOptions
from autobahn.websocket.protocol import parseWsUrl
import txaio

from .serializer import NssJsonSerializer

txaio.use_asyncio()

logger = logging.getLogger(__name__)


class ClientSession(wamp.ApplicationSession):
    "A wamp session that does only care for the authentication"

    def onChallenge(self, challenge):
        return self.config.extra['password']

    def onConnect(self):
        self.join(self.config.realm, ['ticket'],
                  self.config.extra['username'])

    def onJoin(self, details):
        joined = self.config.extra['joined']
        joined.set_result((self, details))

    def onLeave(self, details):
        self.disconnect()
        joined = self.config.extra['joined']
        if details.reason == 'raccoon.error.invalid_user':
            joined.set_exception(
                ValueError('Wrong username or password'))
        elif details.reason == 'wamp.error.no_such_procedure':
            joined.set_exception(
                RuntimeError('Server frontend process appears to be down'))

    async def call(self, procedure, *args, **kw):
        kw['options'] = CallOptions(disclose_me=True)
        return await super().call(procedure, *args, **kw)


class Client(wamp.ApplicationRunner):
    """A client that doesn't own the loop while running"""

    def __init__(self, url, realm, loop=None, ssl=None, **kw):
        kw['serializers'] = [NssJsonSerializer()]
        super().__init__(url, realm, **kw)
        self.loop = loop or asyncio.get_event_loop()
        self.ssl = ssl

    async def connect(self, username, password):
        logger.debug("Connecting to crossbar as %s:%s...", username, password)
        isSecure, host, port, resource, path, params = parseWsUrl(self.url)

        if self.ssl is None:
            ssl = isSecure
        else:
            if self.ssl and not isSecure:
                raise RuntimeError(
                    'ssl argument value passed to %s conflicts with'
                    ' the "ws:" prefix of the url argument.'
                    ' Did you mean to use "wss:"?' %
                    self.__class__.__name__)
            ssl = self.ssl

        joined = asyncio.Future(loop=self.loop)

        def session_factory():
            cfg = ComponentConfig(self.realm, self.extra)
            cfg.extra['username'] = username
            cfg.extra['password'] = password
            cfg.extra['joined'] = joined
            return ClientSession(cfg)

        # create a WAMP-over-WebSocket transport client factory
        transport_factory = WampWebSocketClientFactory(
            session_factory, url=self.url, serializers=self.serializers)

        # start the client
        transport, protocol = await self.loop.create_connection(
            transport_factory, host, port, ssl=ssl)

        self.protocol = protocol
        return await joined

    async def disconnect(self):
        if self.protocol._session:
            await self.protocol.session.leave()
