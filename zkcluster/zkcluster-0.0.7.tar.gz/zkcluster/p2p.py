"""A P2P "Peer" implementation that rides on top of the
RemoteStatusServer / StatusClient system.

It knows only about sending and receiving data on a TCP socket; other
details as far as connecting, receiving connections, and disconnecting
are handled by the RemoteStatusServer / StatusClient.

"""
from .client import GreenLocalClient
from . import util
from . import rpc
from . import exc

import logging

log = logging.getLogger(__name__)


class PeerRunner(object):
    name = 'p2p'

    def __init__(self, service):
        self.service = service
        self.rpc_reg = rpc_reg

        self.nodename = self.service.nodename
        self.peernames = [
            n['name'] for n in self.service.service_config['nodes']]

        service.speak_rpc(rpc_reg)
        service.memos['p2p'] = self
        util.event_listen(service, "before_listen", self.before_listen)
        util.event_listen(
            service,
            "client_connection_disconnected",
            self.client_connection_disconnected)

        self.peers = set()
        self.async_suite = self.service.async_suite

    def speak_rpc(self, rpc_reg):
        self.rpc_reg = self.rpc_reg.join(rpc_reg)
        self.service.speak_rpc(rpc_reg)

    @property
    def total_number_of_peers(self):
        return len(self.peernames)

    def broadcast_rpc_to_peers(self, msg):
        for peer in self.peers:
            if peer.connected:
                msg.send(peer.rpc_service)

    def _remove_server_peer(self, peer):
        self.peers.remove(peer)
        self.dispatch.peer_removed(self)

    def _peer_error_received(self, peer, exception):
        self.dispatch.peer_exception_received(peer, exception)

    def before_listen(self, service):
        self.nodename = self.service.nodename
        assert self.nodename is not None

        for peername in self.peernames:
            if peername == self.nodename:
                continue
            elif peername > self.nodename:
                peer = ClientPeer(
                    self,
                    self.nodename,
                    self.service.service_config,
                    self.service.servicename, peername
                )
                peer._start()

    def client_connection_disconnected(
            self, server, client_connection, unexpected, message):
        if 'p2p_peer' in client_connection.memos:
            server_peer = client_connection.memos['p2p_peer']
            server_peer.disconnect()

    def _cmd_peers(self):
        peer_dict = dict(
            (name, False) for name in self.peernames
        )
        peer_dict.update(
            (peer.name, peer.connected) for peer in self.peers
        )
        return [
            "%s - %s" %
            (
                nodename,
                "this peer" if nodename == self.nodename
                else "connected" if peer_dict[nodename]
                else "disconnected"
            )
            for nodename in self.peernames
        ]


class PeerListener(util.EventListener):
    _dispatch_target = PeerRunner

    def new_peer(self, peer):
        pass

    def peer_connected(self, peer):
        pass

    def peer_disconnected(self, peer):
        pass

    def peer_removed(self, peer):
        pass

    def peer_exception_received(self, peer, exception):
        pass


class Peer(object):
    """generic 'peer' object that represents p2p operations on a socket.

    Base is agnostic of whether the connection is a client or server
    connection.

    """

    def __init__(self, handler, our_nodename, their_nodename):
        self.handler = handler
        self.async_suite = self.handler.async_suite
        self.our_nodename = our_nodename
        self.their_nodename = self.name = their_nodename
        self.memos = {}

    def _enter_pool(self):
        self.handler.peers.add(self)
        self.handler.dispatch.new_peer(self)


class ServerPeer(Peer):
    """peer that's connected via server.ClientConnection.

    """
    _init = False

    def __init__(
            self, handler, our_nodename, client_connection,
            their_nodename):
        super(ServerPeer, self).__init__(handler, our_nodename, their_nodename)
        self.client_connection = client_connection
        self.client_connection.memos['p2p_peer'] = self

        self.rpc_service = self.client_connection.rpc_service
        log.info(
            "[%s] received peer connection from %s", self.our_nodename,
            self.their_nodename)
        self._enter_pool()
        self._init = True
        self.handler.dispatch.peer_connected(self)

    @property
    def connected(self):
        return self._init and self.client_connection.connected

    def disconnect(self):
        log.info(
            "[%s] received disconnect from [%s]",
            self.our_nodename,
            self.their_nodename)
        self.handler.dispatch.peer_disconnected(self)
        self.handler._remove_server_peer(self)


class ClientPeer(Peer):
    """peer that's connected via client.LocalClient.

    """

    def __init__(
            self, handler, our_nodename, service_config,
            servicename, their_nodename):
        super(ClientPeer, self).__init__(handler, our_nodename, their_nodename)
        self.client = GreenLocalClient.from_config(
            service_config, servicename, their_nodename)
        self.rpc_service = self.client.speak_rpc(handler.rpc_reg)

        self.client.memos['p2p_peer'] = self

        util.event_listen(
            self.client, "client_connected", self.client_connected)
        util.event_listen(
            self.client, "client_disconnected", self.client_disconnected)

        self.connected = False
        self._enter_pool()

    def _start(self):
        log.info(
            "[%s] attempting to establish peer connection to [%s]",
            self.our_nodename, self.their_nodename
        )

        def status(success, exception, time):
            if not success:
                log.info(
                    "[%s] continuing to attempt connection to [%s], "
                    "%d seconds so far (can't connect: %s)",
                    self.our_nodename,
                    self.their_nodename,
                    time,
                    exception
                )

        self.client.connect_persistent(status_fn=status, notify_every=30)

    def client_connected(self, client):
        response = SetAsPeer(self.our_nodename).send(self.rpc_service)
        log.info(
            "[%s] established peer connection to [%s] - %s",
            self.our_nodename, self.their_nodename, response)
        self.connected = True
        self.handler.dispatch.peer_connected(self)

    def client_disconnected(self, client):
        self.connected = False
        self.handler.dispatch.peer_disconnected(self)


class P2PConsoleCommands(object):
    name = 'p2p'

    def __init__(self, console):
        self.console = console
        self.console.register_cmds_from(self)
        self.rpc_service = console.speak_rpc(rpc_reg)

    def cmd_set_as_peer(self, name):
        return SetAsPeer(name).send(self.rpc_service)

    def cmd_peers(self):
        return Peers().send(self.rpc_service)

rpc_reg = rpc.RPCReg()


@rpc_reg.call()
class Peers(rpc.RPC):
    def receive_request(self, rpc, service_connection):
        p2p = service_connection.server.memos['p2p']
        if p2p is None:
            return ["%s - not p2p" % (service_connection.server.nodename, )]
        else:
            return p2p._cmd_peers()


@rpc_reg.call('name')
class SetAsPeer(rpc.RPC):
    def receive_request(self, rpc, service_connection):
        p2p = service_connection.server.memos['p2p']
        ServerPeer(p2p, p2p.nodename, service_connection, self.name)


@rpc_reg.call()
class IsClustered(rpc.RPC):

    def receive_request(self, rpc, service_connection):
        server = service_connection.server
        nodes = server.service_config['nodes']
        is_clustered = len(nodes) > 1 and \
            'p2p' in server.memos
        return is_clustered


class P2PRpc(rpc.RPC):
    def receive_request(self, rpc, service_connection_or_client):
        try:
            peer = service_connection_or_client.memos['p2p_peer']
        except KeyError:
            raise exc.RPCError(
                "Received P2P RPC message from client that didn't "
                "send setaspeer: %s, %s" %
                (service_connection_or_client, self)
            )
        else:
            return self.receive_peer_request(rpc, peer)

    def receive_peer_request(self, rpc, peer):
        raise NotImplementedError()


