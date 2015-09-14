from iai.Controller import Controller
from iai.utilities import *
import re


class Axis(object):
    def __init__(self, controller, number_in_controller=1):
        """
        @type controller: Controller
        """
        self._controller = controller
        self.axis_mode = 1 << (number_in_controller - 1)
        self.number = number_in_controller

    def go_home(self, search_speed=0, creep_speed=0):
        raise NotImplementedError

    def wait_for_going_home(self):
        wait(lambda: self.get_status()["axis status"]["Origin return"] == "Returning to Origin")

    def move_absolute(self, position, acceleration, deceleration, speed):
        raise NotImplementedError

    def wait_for_axis_is_using(self):
        wait(lambda: self.get_status()["axis status"]["Servo axis in use"])

    def get_status(self):
        raise NotImplementedError

    def send_command(self, command):
        self._controller.send_command(command)

    def receive_command(self):
        return self._controller.receive_command()


class SSELAxis(Axis):
    def __init__(self, controller, number_in_controller=1):
        super(SSELAxis, self).__init__(controller, number_in_controller)
        self.jogging = False
        pass

    def halt(self):
        command = "![station]HLT "
        command += str(self.axis_mode)
        self.send_command(command)
        self.receive_command()
        self.jogging = False


    def jog(self, speed=100, positive_direction=True, acceleration=0.3):
        if self.jogging == False:
            self.jogging = True
            command = "![station]JOG "
            command += str(self.axis_mode)
            command += "%1.2f " % acceleration
            command += "%03g" % speed
            command += "1" if positive_direction else "0"
            self.send_command(command)
            self.receive_command()

    def move_absolute(self, position, acceleration, deceleration, speed):
        command = "![station]MOV "
        command += str(self.axis_mode)
        command += "%1.2f" % acceleration
        command += " "
        command += "%03g" % speed
        command += " "
        command += ("%3.3f" % position).zfill(7)
        self.send_command(command)
        self.receive_command()
        pass

    def get_status(self):
        command = "?[station]STA"
        command = self._controller.add_controller_info(command)
        command += int_to_upper_hex(calculate_check_sum(command))
        command += "\r\n"
        self.send_command(command)
        status_raw = self.receive_command()
        status_raw = re.findall("STA.(.*)", status_raw)
        status_raw = status_raw[0].split()[:-1]
        status_raw = status_raw[self.number - 1]
        status = {}
        status["axis status"] = {}
        status["axis status"]["raw"] = status_raw[:5]
        status["axis status"]["Servo"] = status_raw[0] == "1"
        status["axis status"]["Servo axis in use"] = status_raw[2] == "1"
        status["axis position"] = float(status_raw[5:])
        return status

    def wait_for_going_home(self):
        Axis.wait_for_axis_is_using(self)

    def wait_for_axis_is_using(self):
        Axis.wait_for_axis_is_using(self)

    def send_command(self, command):
        self._controller.send_command(command)

    def go_home(self, search_speed = 0, creep_speed=0):
        command = "![station]HOM "
        command += str(self.axis_mode) + " "
        command += str(0)
        self.send_command(command)
        self.receive_command()
        # debug_print(command)
        # debug_print(self.receive_command())


class RCPAxis(Axis):
    def __init__(self, controller, number_in_controller=1):
        super(RCPAxis, self).__init__(controller, number_in_controller)
        pass

    def go_home(self, search_speed=0, creep_speed=0):
        command = "![station]"
        command += "233"
        command += int_to_upper_hex(self.axis_mode, 2)  # The axis number in the controller.
        command += int_to_upper_hex(search_speed, 3)  # unit is mm/sec
        command += int_to_upper_hex(creep_speed, 3)  # unit is mm/sec
        self.send_command(command)
        # debug_print(self.receive_command())
        pass

    def wait_for_going_home(self):
        wait(lambda: self.get_status()["axis status"]["Origin return"] == "Returning to Origin")

    def move_absolute(self, position, acceleration, deceleration, speed):
        command = "![station]"  # The %s is the place for the controller's station number.
        command += "234"  # The movement command ID.
        command += int_to_upper_hex(self.axis_mode, 2)  # The axis number in the controller.
        command += int_to_upper_hex(acceleration / 0.01, 4)  # Acceleration's unit is 0.01G
        command += int_to_upper_hex(deceleration / 0.01, 4)  # unit is 0.01G
        command += int_to_upper_hex(speed, 4)  # unit is mm/sec
        command += int_to_upper_hex(position / 0.001, 8)  # Position's unit is 0.001mm
        # command += int_to_upper_hex(position / 0.001, 8)        # The follow axises' position use the same format.
        # command += int_to_upper_hex(position / 0.001, 8)        # The follow axises' position use the same format.
        self.send_command(command)
        # debug_print(self.receive_command())

    def wait_for_axis_is_using(self):
        wait(lambda: self.get_status()["axis status"]["Servo axis in use"])

    def get_status(self):
        self.send_command("![station]21201")
        # TODO: Make all the status bits readable.
        status_raw = self.receive_command()
        status = {"axis status": {}}
        status["axis status"]["raw"] = int(status_raw[8:10], base=16)
        status["axis status"]["Push error detection"] = status["axis status"]["raw"] & 0x20 > 0
        status["axis status"]["Operation command completed"] = status["axis status"]["raw"] & 0x10 > 0
        status["axis status"]["Servo"] = status["axis status"]["raw"] & 0x08 > 0
        status["axis status"]["Origin return"] = (status["axis status"]["raw"] & 0x06) >> 1
        if status["axis status"]["Origin return"] == 0:
            status["axis status"]["Origin return"] = "Not yet performed"
        elif status["axis status"]["Origin return"] == 1:
            status["axis status"]["Origin return"] = "Returning to Origin"
        elif status["axis status"]["Origin return"] == 2:
            status["axis status"]["Origin return"] = "Completed"
        status["axis status"]["Servo axis in use"] = status["axis status"]["raw"] & 0x01 > 0
        return status


