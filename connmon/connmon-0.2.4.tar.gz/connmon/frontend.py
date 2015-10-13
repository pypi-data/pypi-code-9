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


_config_elements = [
    _config.ConfigElement("csv_dump"),
    _config.ConfigElement("csv_token", default="connmon"),
    _config.ConfigElement("csv_columns", _config.StringListFixer, default=[
        "timestamp", "token", "hostname", "progname", "process_count",
        "connection_count", "checkout_count", "max_process_count",
        "max_connections", "max_checkedout"
    ])
]


def load_config(config_file=None, logging_=True):
    if config_file:
        cfg_file = config_file
    else:
        cfg_file = "/etc/connmon.cfg"
        if not os.access(cfg_file, os.F_OK):
            cfg_file = None

    if cfg_file:
        config = _config.Config.from_config_file(
            cfg_file, prefix="connmon_", config_elements=_config_elements)
        if logging_:
            config.load_logging_configs()
    else:
        config = _config.Config.from_config_string("""
[connmon_service_default]
name: default

nodes:
    node1 hostname=localhost:5800 bind=0.0.0.0
""", prefix="connmon_", config_elements=_config_elements)
        if logging_:
            logging.basicConfig()
            logging.getLogger("connmon").setLevel(logging.INFO)
            logging.getLogger("zkcluster").setLevel(logging.INFO)

    return config


class SingleCmdLine(_cmdline.SingleCmdLine):

    def load_config(self):
        if self.options.logging:
            self.cmd.logging = True

        self.config = load_config(
            self.options.config, logging_=self.cmd.logging)


class ListenCmd(_cmdline.ListenCmd):
    logging = True

    def init_server(self, server):
        _server.init_server(server)


def init_client(client):
    client.speak_rpc(_server.rpc_reg)


def client_connected(client):
    stats = _stats.QueuedStats(_green=False)
    with stats.receive_mutex:
        client.memos['stats'] = stats
        summary = _server.InitConsoleRPC().send(client.rpc_service)
        stats.summary_added(summary)
    stats.start()


class MonitorCmd(_cmdline.ClientCmd):
    logging = False

    def create_subparser(self, parser, subparsers):
        return subparsers.add_parser(
            "monitor",
            help="run live monitor")

    def setup_arguments(self, parser):
        super(MonitorCmd, self).setup_arguments(parser)
        parser.add_argument(
            "--dump-only", action="store_true",
            help="dump messages only")
        parser.add_argument(
            "--logging", action="store_true",
            help="enable logging")
        return parser

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

            if cmdline.options.dump_only:
                self._run_dumper(client)
            else:
                self._run_monitor(client)

    def _run_monitor(self, client):
        def on_disconnect(client):
            self.display.stop()
            print("Client connection lost")

        util.event_listen(
            client, "client_disconnected", on_disconnect)
        stats = client.memos['stats']
        self.display = _display.Display(stats, client)
        self.display.start()
        client.close()

    def _run_dumper(self, client):
        def message_received(msg):
            print("Message: %s" % (msg, ))

        def on_disconnect(self, client):
            self.display.stop()
            print("Client connection lost")

        stats = client.memos['stats']
        util.event_listen(stats, "message_received", message_received)

        import time
        self.connected = True
        while self.connected:
            time.sleep(1)


def monitor(argv=None):
    SingleCmdLine(MonitorCmd()).main(argv)


def connmond(argv=None):
    SingleCmdLine(ListenCmd()).main(argv)
