from zymbit.commands import Command
from zymbit.provision import Provision


class ProvisionCommand(Command):
    command_name = 'provision'

    @classmethod
    def setup_parser(cls, parser):
        command_parser = super(ProvisionCommand, cls).setup_parser(parser)

        command_parser.add_argument('--api-url')
        command_parser.add_argument('--websocket-url')
        command_parser.add_argument('--ssl-ignore-hostname', action='store_true')
        command_parser.add_argument('--config-only', action='store_true', help='only write config and exit')
        command_parser.add_argument('--clean', action='store_true', help='remove existing config')
        command_parser.add_argument('token')

        return command_parser

    def run(self):
        token = self.args.token
        api_url = self.args.api_url
        websocket_url = self.args.websocket_url
        check_hostname = not self.args.ssl_ignore_hostname
        config_only = self.args.config_only
        clean = self.args.clean

        provision = Provision(
            token,
            api_url=api_url,
            websocket_url=websocket_url,
            check_hostname=check_hostname,
            config_only=config_only,
            clean=clean
        )
        provision.run()
