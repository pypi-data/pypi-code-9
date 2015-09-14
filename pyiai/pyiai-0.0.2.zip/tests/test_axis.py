from iai import Controller, Axis, Space
import unittest
from mock import MagicMock


class TestRCPAxis(unittest.TestCase):
    def setUp(self):
        self.controller = Controller.RCPController()
        self.controller._serial = MagicMock()
        self.axis = Axis.RCPAxis(self.controller, 1)

    def test_move_absolute(self):
        self.axis.move_absolute(50, 0.3, 0.3, 100)
        self.controller._serial.write.assert_called_once_with(b"!9923401001E001E00640000C350@@\r\n")

    def test_go_home(self):
        self.axis.go_home(64, 0)
        self.controller._serial.write.assert_called_once_with(b"!9923301040000@@\r\n")

    def test_get_status(self):
        self.controller._serial.readline.return_value = b"#99212010C000000000049B2@@\r\n"
        status = self.axis.get_status()
        self.controller._serial.write.assert_called_once_with(b"!9921201@@\r\n")
        self.assertEqual(status["axis status"]["raw"], 0x0c)
        self.assertEqual(status["axis status"]["Push error detection"], False)
        self.assertEqual(status["axis status"]["Operation command completed"], False)
        self.assertEqual(status["axis status"]["Servo"], True)
        self.assertEqual(status["axis status"]["Origin return"], "Completed")
        self.assertEqual(status["axis status"]["Servo axis in use"], False)


class TestSSELAxis(unittest.TestCase):
    def setUp(self):
        self.controller = Controller.SSELController()
        self.controller._serial = MagicMock()
        self.axis = Axis.SSELAxis(self.controller, 1)

    def test_move_absolute(self):
        self.axis.move_absolute(200, 0.3, 0.3, 100)
        self.controller._serial.write.assert_called_once_with(b"!99MOV 10.30 100 200.000B8\r\n")

    def test_go_home(self):
        self.axis.go_home()
        self.controller._serial.write.assert_called_once_with(b"!99HOM 1 018\r\n")

    def test_get_status(self):
        self.controller._serial.readline.return_value = b"#99STA411000100.000  1110024.370   000004998.997 000004998.995 3B\r\n"
        status = self.axis.get_status()
        self.controller._serial.write.assert_called(b"?99STA99\r\n")
        self.assertEqual(status["axis status"]["raw"], "11000")
        self.assertEqual(status["axis status"]["Servo"], True)
        self.assertEqual(status["axis status"]["Servo axis in use"], False)
        self.assertEqual(status["axis position"], 100.0)

        self.axis = Axis.SSELAxis(self.controller, 2)
        status = self.axis.get_status()
        self.controller._serial.write.assert_called("?99STA99\r\n")
        self.assertEqual(status["axis status"]["raw"], "11100")
        self.assertEqual(status["axis status"]["Servo"], True)
        self.assertEqual(status["axis status"]["Servo axis in use"], True)
        self.assertEqual(status["axis position"], 24.37)

    def test_jog(self):
        self.axis.jog(100, True, 0.3)
        self.controller._serial.write.assert_called_with(b"!99JOG 10.30 100167\r\n")

        self.axis.halt()
        self.axis.jog(100, False, 0.3)
        self.controller._serial.write.assert_called_with(b"!99JOG 10.30 100066\r\n")

    def test_halt(self):
        self.axis.halt()
        self.controller._serial.write.assert_called_with(b"!99HLT 1CC\r\n")

