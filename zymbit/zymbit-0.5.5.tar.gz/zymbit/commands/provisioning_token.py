import logging

from zymbit.commands import Command
from zymbit.util import get_provisioning_token


class ProvisioningTokenCommand(Command):
    command_name = 'provisioning_token'

    @property
    def logger(self):
        return logging.getLogger(__name__)

    def run(self):
        print get_provisioning_token()
