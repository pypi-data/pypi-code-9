from zkcluster import rpc
from zkcluster import p2p
from zkcluster import util

import logging
import time

from . import stats as _stats
from . import dumper

log = logging.getLogger(__name__)


def init_server(server):
    stat_ = _stats.QueuedStats(_green=True)
    server.speak_rpc(rpc_reg)
    server.memos['stats'] = stat_
    server.memos['consoles'] = set()
    _peer_handler(server)
    _client_broadcaster(server)

    def start_stats(server):
        stat_.start()

    util.event_listen(server, "before_listen", start_stats)
    util.event_listen(
        server, "client_connection_disconnected", client_disconnected)

    if server.service_config.get('csv_dump'):
        dumper.CSVDumper(server)

    return server


def _peer_handler(server):
    stat_ = server.memos['stats']
    p2p_ = p2p.PeerRunner(server)
    p2p_.speak_rpc(rpc_reg)

    def new_peer(peer):
        peer.memos['stats'] = stat_

    def peer_connected(peer):
        evt = _stats.SummaryEvent(
            stat_.detailed_summary(), _stats.DETAILED_SUMMARY)
        msg = P2PStatsMessage(evt)
        msg.send(peer.rpc_service)
        peer.memos['ready_to_send'] = True

    def peer_disconnected(peer):
        peer.memos['ready_to_send'] = False

    def message_received(message):
        msg = P2PStatsMessage(message)
        for peer in p2p_.peers:
            if peer.memos.get('ready_to_send', False):
                msg.send(peer.rpc_service)

    util.event_listen(p2p_, "new_peer", new_peer)
    util.event_listen(p2p_, "peer_connected", peer_connected)
    util.event_listen(p2p_, "peer_disconnected", peer_disconnected)
    util.event_listen(stat_, "message_received", message_received)


def _client_broadcaster(server):
    consoles = server.memos['consoles']

    handler = server.async_suite

    queue = handler.queue()
    hosts = set()

    def hostprog_modified(hostprog):
        if hostprog not in hosts:
            hosts.add(hostprog)
            queue.put(hostprog)

    def process_hosts():
        while True:
            hostprog = queue.get()
            hosts.discard(hostprog)

            message = _stats.ProcessEvent(
                hostprog.hostname, hostprog.progname, None,
                hostprog.shallow_summary(), time.time(),
                _stats.PROCESS_UPDATED
            )
            msg = ConsoleStatsMessage(message)
            for client in consoles:
                msg.send(client.rpc_service)

            handler.sleep(.001)

    util.event_listen(
        server.memos['stats'], "hostprog_modified", hostprog_modified)

    handler.background_thread(process_hosts)


def client_disconnected(server, client_connection, unexpected, message):
    if 'client_info' in client_connection.memos:
        log.info("Stats client %s disconnected", client_connection)
        info = client_connection.memos['client_info']

        stats = info['stats']

        evt = _stats.ProcessEvent(
            info['remote_hostname'],
            info['remote_progname'],
            info['remote_pid'],
            None,
            time.time(), _stats.PROCESS_REMOVED
        )

        stats.receive_message(evt)

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

        evt = _stats.SummaryEvent(self.summary, _stats.DETAILED_SUMMARY)
        stats.receive_message(evt)


@rpc_reg.call("payload")
class StatsMessage(rpc.RPCEvent):
    """Send a stats event from a database client to the server.

    Request is processed server-side.

    """
    def receive_request(self, rpc, service_connection):
        stats = service_connection.memos['client_info']['stats']
        stats.receive_message(
            _stats.evt_from_tuple(self.payload)
        )


@rpc_reg.call("payload")
class P2PStatsMessage(rpc.RPCEvent):
    """Send a stats event from a server peer to another server peer

    Request is processed server-side.

    """
    def receive_request(self, rpc, service_connection):
        stats = service_connection.memos['p2p_peer'].memos['stats']
        stats.receive_message(
            _stats.evt_from_tuple(self.payload)
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
        return stats.shallow_summary()


@rpc_reg.call("payload")
class ConsoleStatsMessage(rpc.RPCEvent):
    """Send a stats event from the server to a listening console.

    Request is processed client-side.

    """
    def receive_request(self, rpc, console):
        with console.memos['stats'].receive_mutex:
            console.memos['stats'].receive_message(
                _stats.evt_from_tuple(self.payload)
            )
