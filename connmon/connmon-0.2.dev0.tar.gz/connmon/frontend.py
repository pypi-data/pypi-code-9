import os
import logging

from zkcluster import config as _config
from zkcluster import client as _client
from zkcluster import cmdline as _cmdline
from zkcluster import exc
from zkcluster import util

from . import stats as _stats
from . import server as _server
from . import display as _display


def load_config(config_file=None):
    if config_file:
        cfg_file = config_file
    else:
        cfg_file = "/etc/connmon.cfg"
        if not os.access(cfg_file, os.F_OK):
            cfg_file = None

    if cfg_file:
        config = _config.Config.from_config_file(
            cfg_file, prefix="connmon_")
        config.load_logging_configs()
    else:
        config = _config.Config.from_config_string("""
[connmon_service_default]
name: default

nodes:
    node1 hostname=localhost:5800 bind=0.0.0.0
""", prefix="connmon_")
        logging.basicConfig()
        logging.getLogger("connmon").setLevel(logging.INFO)
        logging.getLogger("zkcluster").setLevel(logging.INFO)

    return config


class SingleCmdLine(_cmdline.SingleCmdLine):
    def load_config(self):
        self.config = load_config(self.options.config)


class ListenCmd(_cmdline.ListenCmd):
    def init_server(self, server):
        _server.init_server(server)


def init_client(client):
    client.speak_rpc(_server.rpc_reg)


def client_connected(client):
    client.memos['stats'] = stats = _stats.Stats()
    summary = _server.InitConsoleRPC().send(client.rpc_service)
    stats.summary_added(summary)


class MonitorCmd(_cmdline.ClientCmd):
    def create_subparser(self, parser, subparsers):
        return subparsers.add_parser(
            "monitor",
            help="run live monitor")

    def go(self, cmdline):

        args = self.get_client_args(cmdline.options, cmdline.config)

        if "hostname" in args:

            client = _client.LocalClient.from_host_port(
                args['user'], args['password'],
                args['hostname'], args['port'])

        elif "service" in args:
            client = _client.LocalClient.from_config(
                args['service_config'], args['service'],
                args['node'], args['user'], args['password'])

        init_client(client)

        try:
            client.connect()
        except exc.AuthFailedError:
            print("auth failed")
        except exc.DisconnectedError as de:
            print(de)
        else:
            client_connected(client)
            util.event_listen(
                client, "client_disconnected", self.on_disconnect)
            stats = client.memos['stats']
            self.display = _display.Display(stats, client)
            self.display.start()
            client.close()

    def on_disconnect(self, client):
        self.display.stop()
        print("Client connection lost")


def monitor(argv=None):
    SingleCmdLine(MonitorCmd()).main(argv)


def connmond(argv=None):
    SingleCmdLine(ListenCmd()).main(argv)

