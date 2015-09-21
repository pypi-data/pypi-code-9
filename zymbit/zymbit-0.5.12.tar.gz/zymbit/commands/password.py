import logging

from zymbit.commands import Command
from zymbit.common.config import get_config


class PasswordCommand(Command):
    command_name = 'password'

    @property
    def logger(self):
        return logging.getLogger(__name__)

    def run(self):
        config = get_config()

        default_auth = config['auth']['default_auth']
        auth = config['auth'][default_auth]

        print auth['password']
