import argparse
import getpass

from . import config as _config
from . import exc
from . import console as _console
from . import server as _server


class Cmd(object):

    def create_subparser(self, parser, subparsers):
        raise NotImplementedError()

    def setup_arguments(self, parser):
        raise NotImplementedError()

    def go(self, cmdline):
        raise NotImplementedError()


class ListenCmd(Cmd):
    def create_subparser(self, parser, subparsers):
        return subparsers.add_parser(
            "listen",
            help="listen for connections")

    def setup_arguments(self, parser):
        parser.add_argument(
            "-s", "--service", type=str,
            default="default", help="name of service")
        parser.add_argument(
            "-n", "--node", type=str, help="name of service node")
        return parser

    def go(self, cmdline):
        servicename = cmdline.options.service
        nodename = cmdline.options.node

        server_config = cmdline.config.config_for_servicename(servicename)
        server = self.get_server(server_config, servicename, nodename)
        self.init_server(server)
        server.serve_forever()

    def get_server(self, server_config, servicename, nodename):
        return _server.RemoteServer(server_config, servicename, nodename)

    def init_server(self, server):
        pass


class ClientCmd(Cmd):
    def setup_arguments(self, parser):
        parser.add_argument(
            "-s", "--service", type=str,
            default="default",
            help="name of service to connect (exclusive against --host)")
        parser.add_argument(
            "-H", "--host", type=str,
            help="host[:port] to connect (exclusive against --service)"
        )
        parser.add_argument(
            "-n", "--node", type=str,
            help="specific node name to connect to (assumes --service)")
        parser.add_argument(
            "-u", "--user", type=str, help="username")
        parser.add_argument(
            "-p", "--password", type=str, help="password")

    def get_client_args(self, options, config):

        if options.host:
            if options.service not in (None, 'default'):
                raise exc.ServiceException(
                    "Can't send --service argument with --host")
            if options.node:
                raise exc.ServiceException(
                    "Can't send --node argument with --host"
                )
            if ":" in options.host:
                hostname, port = options.host.split(":", 1)
                port = int(port)
            else:
                hostname = options.host
                port = 5800

            if options.user and not options.password:
                password = getpass.getpass("Password:")
            else:
                password = options.password

            return {
                "user": options.user, "password": password,
                "hostname": hostname, "port": port}

        elif options.service:
            service_config = config.config_for_servicename(options.service)
            if options.user and not options.password:
                password = getpass.getpass("Password:")
            else:
                password = options.password

            return {
                "service_config": service_config,
                "service": options.service,
                "node": options.node, "user": options.user,
                "password": password
            }


class ConsoleCmd(ClientCmd):

    def create_subparser(self, parser, subparsers):
        return subparsers.add_parser(
            "console",
            help="console to a service")

    def go(self, cmdline):

        args = self.get_client_args(cmdline.options, cmdline.config)

        if "host" in args:

            client = self.get_console_host_port(
                args['user'],
                args['password'],
                args['hostname'],
                args['port'])

        elif "service" in args:

            client = self.get_console_servicename(
                args['service_config'], args['service'],
                args['node'], args['user'], args['password'])

        self.init_console(client)

        try:
            client.connect()
        except exc.AuthFailedError:
            print("auth failed")
        except exc.DisconnectedError as de:
            print(de)
        else:
            self.console_connected(client)
            self.run_console(client)

    def run_console(self, client):
        client.interact()

    def get_console_servicename(
            self, server_config, servicename, nodename,
            username=None, password=None):
        return _console.Console.from_config(
            server_config, servicename, nodename,
            username=username, password=password)

    def get_console_host_port(self, username, password, hostname, port):
        return _console.Console.from_host_port(
            username, password, hostname, port)

    def console_connected(self, console):
        pass


class CmdLineBase(object):
    def create_parser(self):
        self.parser = argparse.ArgumentParser(prog=self.prog)
        self.parser.add_argument(
            "-c", "--config",
            type=str,
            help="Path to config file")

    def load_config(self):
        if self.options.config:
            self.config = _config.Config.from_config_file(self.options.config)
        else:
            self.config = _config._CFG

        self.config.load_logging_configs()

    def run(self):
        raise NotImplementedError()

    def main(self, argv=None, prog=None):
        self.options = self.parser.parse_args(argv)

        self.load_config()

        self.run(self.options, self.config)


class SingleCmdLine(CmdLineBase):
    def __init__(self, cmd, prog=None):
        self.prog = prog
        self.cmd = cmd
        self.create_parser()
        cmd.setup_arguments(self.parser)

    def run(self, options, config):
        self.cmd.go(self)


class CmdLine(CmdLineBase):
    def __init__(self, cmds=[ListenCmd(), ConsoleCmd()], prog=None):
        self.prog = prog
        self.create_parser()
        self.subparsers = self.parser.add_subparsers()

        for cmd in cmds:
            self.add_cmd(cmd)

    def add_cmd(self, cmd):
        subparser = cmd.create_subparser(self.parser, self.subparsers)
        cmd.setup_arguments(subparser)
        subparser.set_defaults(cmd=cmd)

    def run(self, options, config):
        cmd = options.cmd
        cmd.go(self)

if __name__ == '__main__':
    CmdLine().main()
