import logging

from zymbit.commands import Command
from zymbit.common.config import get_config, save_config


class LogoutCommand(Command):
    command_name = 'logout'

    @property
    def logger(self):
        return logging.getLogger(__name__)

    def run(self):
        config = get_config()

        auth_config = config.get('auth')

        if not auth_config:
            return

        auth_config.pop('default_auth', None)

        keys = auth_config.keys()
        for key in keys:
            if '@' in key and '.' in key:
                auth_config.pop(key)

        save_config(config)
