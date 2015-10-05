import socket
import random
from . import rpc
import time

from . import util
from . import server as _server
from . import exc
import logging

log = logging.getLogger(__name__)


class LocalClient(object):
    def __init__(self, servicename, key, secret, node_configs):
        self.servicename = servicename
        self.key = key
        self.secret = secret
        self.async_suite = self._make_async_suite()
        self.rpc_service = rpc.RPCService(_server.rpc_reg, self)
        self.node_configs = node_configs
        self.connected = False
        self._reconnect_on_disconnect = False
        self.last_ping = util.periodic_timer(_server.Ping.ping_timeout)
        self.memos = {}

    def speak_rpc(self, rpc_reg):
        self.rpc_service.speak_rpc(rpc_reg)
        return self.rpc_service

    def _make_async_suite(self):
        return util.async_suite()

    @classmethod
    def from_multi_host_port(cls, username, password, hosts):
        node_configs = [
            {"hostname": hostname, "port": port}
            for hostname, port in hosts
        ]
        return cls(
            "%s:%s" % (hostname, port),
            username,
            password, node_configs
        )

    @classmethod
    def from_host_port(cls, username, password, hostname, port):
        node_configs = [
            {"hostname": hostname, "port": port}
        ]
        return cls(
            "%s:%s" % (hostname, port),
            username,
            password, node_configs
        )

    @classmethod
    def from_config(
            cls, service_config, servicename,
            nodename=None, username=None, password=None):

        if nodename is None:
            our_nodes = service_config['nodes']
        else:
            nodes = dict(
                (node['name'], node) for node in service_config['nodes']
            )
            try:
                our_nodes = [nodes[nodename]]
            except KeyError:
                raise exc.ServiceException(
                    "no such node name %r" % nodename)

        # TODO: if node is none, send list of all hosts
        key = username or service_config['auth_key']
        secret = password or service_config['auth_secret']
        return cls(servicename, key, secret, our_nodes)

    def connect(self):
        nodes = list(self.node_configs)
        random.shuffle(nodes)
        for node in nodes:
            host = node['hostname']
            port = node['port']
            try:
                self.socket = self.async_suite.create_connection(
                    (host, port), timeout=2)
            except IOError as ioe:
                continue
            else:
                self.connected = True
                self.host = host
                self.port = port
                self.nodename = node['name']
                break

        else:
            raise exc.DisconnectedError(
                "Can't connect to servicename=%r: %s" %
                (self.servicename, ioe)
            )

        self._handle_thread = self.async_suite.background_thread(self._handle)

        self._authenticate()
        self.last_ping.reset(time.time())
        self.dispatch.client_connected(self)

    def connect_persistent(self, status_fn=None, notify_every=None):
        self._reconnect_on_disconnect = True
        self.async_suite.spawn(
            self._connect_persistent,
            status_fn=status_fn, notify_every=notify_every)

    def _connect_persistent(self, status_fn=None, notify_every=None):
        now = started = time.time()
        while not self.connected:
            try:
                self.connect()
            except exc.DisconnectedError as de:
                attempting_for = time.time() - now
                if attempting_for > notify_every:
                    now = time.time()
                    status_fn(False, de, time.time() - started)
                self.async_suite.sleep(1)
            else:
                if status_fn:
                    status_fn(True, None, time.time() - started)
                log.info(
                    "LocalClient connected to host %s:%s",
                    self.host, self.port)
                break

    def on_disconnect(self, unexpected, message):
        if self._reconnect_on_disconnect:
            log.info(
                "LocalClient lost connection to host %s:%s; "
                "reconnecting to servicename=%r",
                self.host, self.port, self.servicename)

            def status(success, exception, time):
                log.info(
                    "Continuing to attempt connection to servicename=%r, "
                    "%d seconds so far (%s)",
                    self.servicename,
                    time,
                    exception
                )
            self.connect_persistent(status_fn=status, notify_every=30)
        else:
            log.info(
                "LocalClient lost connection to host %s:%s",
                self.host, self.port)

    def _handle(self):
        try:
            for message in self.async_suite.receive_messages(
                    self.socket, self._message_terminator,
                    self._check_ping, _server.Ping.ping_interval):
                self.rpc_service.message_received(message)
        except IOError as ioe:
            if self.connected:
                self._close(unexpected=True, message=str(ioe))

    def _authenticate(self):
        try:
            _server.Authenticate(
                self.key, self.secret).send(self.rpc_service)
        except exc.RPCError:
            raise exc.AuthFailedError()

    _message_terminator = "&&OK"

    def _check_ping(self):
        if self.last_ping(time.time()):
            self._close(
                unexpected=True, message="ping timeout, no pong from server")
        else:
            _server.Ping().send_async(
                self.rpc_service,
                callback=self._receive_ping,
                exception_callback=self._ping_failed)

    def _receive_ping(self, message):
        self.last_ping.reset(time.time())

    def _ping_failed(self, exception):
        log.error("ping failed: %s", exception)

    def close(self):
        if self.connected:
            self.connected = False
            self.socket.shutdown(socket.SHUT_RDWR)
            self.socket.close()

    def _close(self, unexpected=False, message=None):
        was_connected = self.connected
        self.connected = False
        if not unexpected:
            self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()
        if was_connected:
            # note: the console looks for this
            # in its on_disconnect handler, so set first
            self.dispatch.client_disconnected(self)
            self.on_disconnect(unexpected, message)

    def send_message(self, message):
        if not self.connected:
            raise exc.DisconnectedError("client is not connected")
        # print "send message", message
        self.socket.sendall(message + self._message_terminator)


class GreenLocalClient(LocalClient):
    def _make_async_suite(self):
        return util.async_suite(green=True)


class ClientListener(util.EventListener):
    _dispatch_target = LocalClient

    def client_connected(self, client):
        pass

    def client_disconnected(self, client):
        pass


