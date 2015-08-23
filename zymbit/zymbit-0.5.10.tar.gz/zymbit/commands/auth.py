import logging

from tabulate import tabulate

from zymbit.commands import Command
from zymbit.compat import config


class StreamsCommand(Command):
    command_name = 'auth'

    @property
    def logger(self):
        return logging.getLogger(__name__)

    def run(self):

        _config = config.get_config()

        email = _config['auth']['default_auth']
        auth = _config['auth'][email]

        headers = ['email', 'password', 'auth_token']
        table = [[email, auth['password'], auth['auth_token']]]

        print tabulate(table, headers=headers)
