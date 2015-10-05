import logging
import time

from . import util
from . import rpc
from . import exc


log = logging.getLogger(__name__)


class RemoteServer(util.Startable):
    def __init__(self, service_config, servicename, nodename):
        self.service_config = service_config
        self.servicename = servicename
        self.nodename = nodename
        self.async_suite = util.async_suite(green=True)
        self.use_auth = self.service_config['use_auth']
        self.memos = {}
        self.rpc_reg = rpc_reg

    def speak_rpc(self, rpc_reg):
        self.rpc_reg = self.rpc_reg.join(rpc_reg)

    def serve_forever(self):
        if self.nodename is None:
            if len(self.service_config['nodes']) > 1:
                raise exc.ServiceException(
                    "--node is required; choose one of %s" %
                    ", ".join(node['name'] for node
                              in self.service_config['nodes']))
            else:
                our_node = self.service_config['nodes'][0]
                self.nodename = our_node['name']
        else:
            nodes = dict(
                (node['name'], node) for node in self.service_config['nodes']
            )
            try:
                our_node = nodes[self.nodename]
            except KeyError:
                raise exc.ServiceException(
                    "no such node name %r" % self.nodename)

        bind_address = our_node['bind']
        bind_port = our_node.get('bind_port', None) or our_node['port']

        self.connections = set()

        if self.service_config['ssl_keyfile']:
            ssl_args = {
                'keyfile': self.service_config['ssl_keyfile'],
                'certfile': self.service_config['ssl_certfile'],
                'do_handshake_on_connect': True
            }
        else:
            ssl_args = {}

        self.server = self.async_suite.server(
            (bind_address, bind_port), self._connected, **ssl_args
        )
        log.info(
            "Listening on %saddress %s port %d",
            "SSL " if ssl_args else "", bind_address, bind_port)

        self.dispatch.before_listen(self)

        self.server.serve_forever()

    def _auth_key_secret(self, key, secret):
        auth_key = self.service_config['auth_key']
        auth_secret = self.service_config['auth_secret']

        return key == auth_key and secret == auth_secret

    def _connected(self, socket, address):
        ClientConnection(self, socket, address)


class ClientConnection(object):
    # TODO: would like to use __slots__ here once we can stablize the API

    _message_terminator = "&&OK"

    def __init__(self, server, socket, address):
        self.server = server
        self.socket = socket
        self.address = address
        self.username = None
        server.connections.add(self)
        log.info("%s", self)
        self.async_suite = server.async_suite
        self.rpc_service = rpc.RPCService(server.rpc_reg, self)
        self._authenticated = False
        self.connected = True
        self.memos = {}
        self.last_ping = util.periodic_timer(Ping.ping_timeout)
        self.last_ping.reset(time.time())
        self.greenlet = self.async_suite.spawn(self._handle, socket)
        self.server.dispatch.client_connection_connected(self.server, self)

    def send_message(self, message):
        if not self.connected:
            raise exc.DisconnectedError("not connected")
        self.socket.sendall(message + self._message_terminator)

    def broadcast_rpc_to_clients(self, msg, filter_fn=None):
        """Send an RPC to all external clients."""

        for server_connection in self.service.connections:
            if filter_fn and not filter_fn(server_connection):
                pass
            msg.send_event(self.rpc_service)

    def _handle(self, socket):
        try:
            for message in self.server.async_suite.receive_messages(
                    self.socket, self._message_terminator,
                    self._check_ping, Ping.ping_interval):

                if not self._authenticated:
                    if not self._authenticate(message):
                        break
                else:
                    self.rpc_service.message_received(message)
        except self.async_suite.interrupted:
            self._close()
        except IOError as ioe:
            self._close(unexpected=True, message=str(ioe))
        else:
            self._close()

    def _check_ping(self):
        if self.last_ping(time.time()):
            raise IOError("ping timeout, no ping from client")

    def _receive_ping(self):
        self.last_ping.reset(time.time())
        return "PONG"

    def _authenticate(self, message):
        self.rpc_service.message_received(
            message, expected=Authenticate)
        if self._authenticated:
            log.info("Authenticated connection from %r", self.username)
            self.server.dispatch.client_connection_authenticated(
                self.server, self)
        else:
            log.info("Authentication failed for username %r", self.username)
        return self._authenticated

    def _cmd_authenticate(self, key, secret):
        self.username = key
        auth = not self.server.use_auth or \
            self.server._auth_key_secret(key, secret)
        if auth:
            self._authenticated = True
            return [
                "Service name: %s" % self.server.servicename
            ]
        else:
            raise exc.AuthFailedError()

    def _cmd_servicename(self):
        return self.server.servicename

    def _cmd_quit(self):
        self.greenlet.kill()

    def __str__(self):
        return "ClientConnection(%s:%s)" % self.address

    def _close(self, unexpected=False, message=None):
        self.server.connections.discard(self)
        if not unexpected:
            self.socket.shutdown(self.async_suite.socket.SHUT_RDWR)
        self.socket.close()
        self.connected = False
        self.server.dispatch.client_connection_disconnected(
            self.server, self, unexpected, message)
        log.info("%s closed (%s)", self, message)


class ServerListener(util.EventListener):
    _dispatch_target = RemoteServer

    def before_listen(self, server):
        pass

    def client_connection_connected(self, server, client_connection):
        pass

    def client_connection_authenticated(self, server, client_connection):
        pass

    def client_connection_disconnected(
            self, server, client_connection, unexpected, message):
        pass

rpc_reg = rpc.RPCReg()


@rpc_reg.call('key', 'secret')
class Authenticate(rpc.RPC):
    def receive_request(self, rpc, service_connection):
        return service_connection._cmd_authenticate(self.key, self.secret)


@rpc_reg.call()
class Ping(rpc.RPC):
    ping_timeout = 30
    ping_interval = 15

    def receive_request(self, rpc, service_connection):
        return service_connection._receive_ping()


@rpc_reg.call()
class Servicename(rpc.RPC):
    def receive_request(self, rpc, service_connection):
        return service_connection._cmd_servicename()


@rpc_reg.call()
class Quit(rpc.RPC):
    def receive_request(self, rpc, service_connection):
        return service_connection._cmd_quit()

