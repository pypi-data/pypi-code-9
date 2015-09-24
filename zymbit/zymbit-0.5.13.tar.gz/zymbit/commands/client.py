import code
import logging
import readline
import rlcompleter
import threading
import time

from zymbit.commands import Command
from zymbit.client import Client


class Printer(object):
    def __init__(self, client):
        self.client = client
        self._run = True

    def loop(self):
        data = self.client.recv()
        if data:
            print data
            return True

    def quit(self):
        self._run = False

    def run(self):
        while self._run:
            try:
                got_data = self.loop()
            except Exception:
                break

            if not got_data:
                time.sleep(1.0)


class ClientCommand(Command):
    command_name = 'client'

    @property
    def logger(self):
        return logging.getLogger(__name__)

    def run(self):
        client = Client()
        printer = Printer(client)

        self.thread = threading.Thread(target=printer.run)
        self.thread.start()

        vars = locals()

        readline.set_completer(rlcompleter.Completer(vars).complete)
        readline.parse_and_bind("tab: complete")

        console = code.InteractiveConsole(vars)

        try:
            console.interact()
        except KeyboardInterrupt:
            pass
        finally:
            printer.quit()
