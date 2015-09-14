from iai.utilities import *
import platform
import sys

is_py3 = sys.version[0] == '3'

class Controller(object):
    def __init__(self, port=None, baudrate=None, timeout=5, station=0x99):
        self.station = station
        self.is_ironpython = platform.python_implementation() == "IronPython"
        if port and baudrate:
            if self.is_ironpython:
                import clr
                clr.AddReference('System')
                import System
                self._serial = System.IO.Ports.SerialPort(port)
                self._serial.BaudRate = baudrate
                self._serial.DataBits = 8
                self._serial.Open()
                self._serial.write = self._serial.Write
                self._serial.readline = self._serial.ReadLine
            else:
                import serial
                self._serial = serial.Serial(port, baudrate, timeout=timeout)
            self.send_init_command()

    def add_controller_info(self, command):
        """

        :type command: str
        """
        return command.replace("[station]", int_to_upper_hex(self.station, 2))

    def send_init_command(self):
        self.send_command("?[station]VERM0")
        self.receive_command()

    def send_command(self, command):
        command = self.add_controller_info(command)
        command += int_to_upper_hex(calculate_check_sum(command), 2)
        command += "\r\n"
        command = command.encode()
        self._serial.write(command)

    def receive_command(self, timeout=None):
        if timeout:
            self._serial.timeout = timeout
        received = self._serial.readline()

        if is_py3:
            return received.decode("UTF-8")
        else:
            return str(received)

        return received

    def close(self):
        self._serial.close()

class RCPController(Controller):
    def send_command(self, command):
        command = self.add_controller_info(command)
        command += "@@" # Check sum use the '@@' in the master.
        command += "\r\n"
        command = command.encode()
        self._serial.write(command)

class SSELController(Controller):
    pass