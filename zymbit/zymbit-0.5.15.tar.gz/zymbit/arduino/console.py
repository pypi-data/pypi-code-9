import logging
import socket
import time
from zymbit.exceptions import ConnectionError

from zymbit.linux.console import Console

from subprocess import PIPE, STDOUT, Popen

DEFAULT_HOST = 'localhost'
DEFAULT_PORT = 6571


class ArduinoConsole(Console):
    @property
    def logger(self):
        return logging.getLogger(__name__)

    def connected(self, host_info):
        super(ArduinoConsole, self).connected(host_info)

        self.logger.debug('connected to host_info={}'.format(host_info))

    def _restart_bridge(self):
        """
        Checks to see if the bridge process is running
        :return: boolean - whether the bridge was restarted
        """
        running = self._is_bridge_running()
        if not running:
            self.logger.warning('bridge not running, resetting mcu')
            status = Popen('/usr/bin/reset-mcu').wait()
            self.logger.info('reset-mcu status={}'.format(status))

            for i in range(10):  # wait for bridge to show up
                running = self._is_bridge_running()
                if running:
                    break

                time.sleep(1.0)
            else:
                self.logger.warning('bridge still not found in process listing')

            if running:  # let the bridge settle for a couple seconds
                time.sleep(2.0)

            return running

        return False

    def handle_socket_exception(self, socket_exc):
        """
        Handle the socket exception
        :param socket_exc: Exception
        """
        super(ArduinoConsole, self).handle_socket_exception(socket_exc)

        # try to restart the bridge on arduinos and if successful, try reopening the socket
        if self._restart_bridge():
            return self.socket

    def _is_bridge_running(self):
        """
        Check to see if bridge is running
        :return: Boolean
        """
        command = 'ps'

        proc = Popen(command, stdout=PIPE, stderr=STDOUT)
        stdout, _ = proc.communicate('')

        running = 'python -u bridge.py' in stdout

        return running


class ArduinoConsoleTask(ArduinoConsole):
    """
    Subclass that relays all arduino messages to the cloud messenger
    """
    def __init__(self, host=DEFAULT_HOST, port=DEFAULT_PORT):
        super(ArduinoConsoleTask, self).__init__(host, port)

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.addr = ('localhost', 9628)

    @property
    def logger(self):
        name = '{}.{}'.format(__name__, self.__class__.__name__)

        return logging.getLogger(name)

    def loop(self):
        # TODO: add a buffer to store messages that cannot be sent
        try:
            buf = self.recv(0.1)
        except ConnectionError, exc:
            self.handle_socket_exception(exc)
        else:
            if not buf:
                return

            for line in buf.splitlines():
                self.logger.debug('sending line={} to addr={}'.format(line, self.addr))
                try:
                    self.sock.sendto(line, self.addr)
                except socket.error, exc:
                    self.logger.exception(exc)
                    self.logger.error('unable to send buf={}'.format(buf))

                    self.handle_socket_exception(exc)
