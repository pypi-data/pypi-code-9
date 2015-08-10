__author__ = 'sinisa'

import inject
import sbg_cli.sbg_docker.commands
from sbg_cli.sbg_docker import production
from sbg_cli.command import Utility, get_commands, create_usage_string


class Docker(Utility):

    def __init__(self, basecmd):
        super(Docker, self).__init__(basecmd)
        inject.configure(production)
        self.commands = get_commands(sbg_cli.sbg_docker.commands)
        self.USAGE = create_usage_string(self.USAGE, self.basecmd, self.commands)

    def __call__(self, *args, **kwargs):
        self.commands[args[0]](**kwargs)
