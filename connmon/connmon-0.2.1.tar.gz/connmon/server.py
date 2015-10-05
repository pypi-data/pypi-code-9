from zkcluster import rpc
from zkcluster import p2p
from zkcluster import util

import logging
from . import stats
from . import dumper

log = logging.getLogger(__name__)


def init_server(server):
    stat_ = stats.QueuedStats()
    server.speak_rpc(rpc_reg)
    server.memos['stats'] = stat_
    server.memos['consoles'] = consoles = set()
    p2p_ = p2p.PeerRunner(server)
    p2p_.speak_rpc(rpc_reg)

    def message_received(message):
        # broadcast stats events to listening consoles

        msg = ConsoleStatsMessage(message)
        for client in consoles:
            msg.send(client.rpc_service)

    def new_peer(peer):
        peer.memos['stats'] = stat_

    def peer_connected(peer):
        evt = stats.SummaryEvent(stat_.summary(), stats.SUMMARY)
        msg = P2PStatsMessage(evt)
        msg.send(peer.rpc_service)

    def start_stats(server):
        stat_.start()

    util.event_listen(server, "before_listen", start_stats)
    util.event_listen(
        server.memos['stats'], "message_received", message_received)
    util.event_listen(p2p_, "new_peer", new_peer)
    util.event_listen(p2p_, "peer_connected", peer_connected)
    util.event_listen(
        server, "client_connection_disconnected", client_disconnected)

    if server.service_config.get('csv_dump'):
        dumper.CSVDumper(server)

    return server


def client_disconnected(server, client_connection, unexpected, message):
    if 'client_info' in client_connection.memos:
        log.info("Stats client %s disconnected", client_connection)
        info = client_connection.memos['client_info']

        stats = info['stats']
        evt = stats.process_closed(
            info['remote_hostname'],
            info['remote_progname'],
            info['remote_pid']
        )

        msg = P2PStatsMessage(evt)
        p2p_ = client_connection.server.memos['p2p']
        p2p_.broadcast_rpc_to_peers(msg)

    elif 'console' in client_connection.memos:
        log.info("Console client %s disconnected", client_connection)
        server.memos['consoles'].remove(client_connection)


rpc_reg = rpc.RPCReg()


@rpc_reg.call("remote_hostname", "remote_progname", "remote_pid", "summary")
class InitClientRPC(rpc.RPCEvent):
    """Initial rpc call sent from a database client to the server.

    Identifies the client as a database listener which will send us events.

    Request is processed server-side.

    """

    def receive_request(self, rpc, service_connection):
        log.info("New stats client %s", service_connection)

        stats = service_connection.server.memos['stats']
        service_connection.memos['client_info'] = {
            'remote_hostname': self.remote_hostname,
            'remote_progname': self.remote_progname,
            'remote_pid': self.remote_pid,
            'stats': stats
        }

        evt = stats.summary_added(self.summary)

        msg = P2PStatsMessage(evt)
        p2p_ = service_connection.server.memos['p2p']
        p2p_.broadcast_rpc_to_peers(msg)


@rpc_reg.call("payload")
class StatsMessage(rpc.RPCEvent):
    """Send a stats event from a database client to the server.

    Request is processed server-side.

    """
    def receive_request(self, rpc, service_connection):
        stats_ = service_connection.memos['client_info']['stats']
        stats_.receive_message(
            stats.evt_from_tuple(self.payload)
        )

        msg = P2PStatsMessage(self.payload)
        p2p_ = service_connection.server.memos['p2p']
        p2p_.broadcast_rpc_to_peers(msg)


@rpc_reg.call("payload")
class P2PStatsMessage(rpc.RPCEvent):
    """Send a stats event from a server peer to another server peer

    Request is processed server-side.

    """
    def receive_request(self, rpc, service_connection):
        stats_ = service_connection.memos['p2p_peer'].memos['stats']
        stats_.receive_message(
            stats.evt_from_tuple(self.payload)
        )


@rpc_reg.call()
class InitConsoleRPC(rpc.RPC):
    """Initial rpc call sent from a console client to the server.

    Identifies the client as a console, which will receive events from
    the server.

    Request is processed server-side.

    """

    def receive_request(self, rpc, service_connection):
        log.info("New console client %s", service_connection)

        server = service_connection.server   # RemoteServer instance

        service_connection.memos['console'] = True
        consoles = server.memos['consoles']
        consoles.add(service_connection)

        stats = server.memos['stats']
        return stats.summary()


@rpc_reg.call("payload")
class ConsoleStatsMessage(rpc.RPCEvent):
    """Send a stats event from the server to a listening console.

    Request is processed client-side.

    """
    def receive_request(self, rpc, console):
        console.memos['stats'].receive_message(
            stats.evt_from_tuple(self.payload)
        )

