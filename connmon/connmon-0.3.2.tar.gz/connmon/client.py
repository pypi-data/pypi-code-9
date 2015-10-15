import os
from . import stats
import logging
from . import server
from . import frontend as _frontend
from zkcluster import client as _client
from zkcluster import util
log = logging.getLogger(__name__)


class StatsClient(object):
    def __init__(self, client, hostname, progname, pid):
        self.hostname = hostname
        self.progname = progname
        self.pid = pid
        self.connected = False
        self.local_state = stats.RemotePid(hostname, progname, pid)

        self.async_suite = util.async_suite(green=False)
        self.send_mutex = self.async_suite.lock()

        self.client = client
        self.rpc_service = self.client.speak_rpc(server.rpc_reg)
        util.event_listen(self.client, "client_connected", self.on_connect)
        util.event_listen(
            self.client, "client_disconnected", self.on_disconnect)
        self.client.connect_persistent()

    @classmethod
    def from_connect_info(cls, connect_info, hostname, progname, pid):

        if 'service' in connect_info:
            servicename = connect_info['service']
            config = _frontend.load_config(connect_info['config'])
            service_config = config.config_for_servicename(
                connect_info['service'])
            client = _client.LocalClient.from_config(
                service_config, servicename, receive_events=False)
        elif 'host' in connect_info:
            host = connect_info['host']
            port = connect_info['port']
            client = _client.LocalClient.from_host_port(
                None, None, host, port, receive_events=False)
        else:
            raise ValueError("'service' or 'host' expected")

        return StatsClient(client, hostname, progname, pid)

    def on_connect(self, client):
        with self.send_mutex:
            server.InitClientRPC(
                self.hostname,
                self.progname,
                self.pid,
                self.local_state.detailed_summary()
            ).send(self.rpc_service)
            self.connected = True

    def on_disconnect(self, client):
        self.connected = False

    def send(self, evt):
        assert self.pid == os.getpid()

        with self.send_mutex:
            self.local_state.receive_message(evt)
            # note this is different from self.client.connected
            if self.connected:
                server.StatsMessage(evt).send(self.rpc_service)

    def close(self):
        raise NotImplementedError()
