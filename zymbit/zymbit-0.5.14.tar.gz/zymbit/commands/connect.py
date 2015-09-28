import logging

from zymbit.commands import Command
from zymbit.connector import get_connector


class ConnectCommand(Command):
    command_name = 'connect'

    @property
    def logger(self):
        return logging.getLogger(__name__)

    def run(self):
        connector = get_connector()

        try:
            while True:
                connector.run()
        except KeyboardInterrupt:
            connector.quit()
