import glob
import sys

import serial


def get_available_usb():
    """
        Return a list of available serial USB port, works on win, macosx and linux

    :return: list of available serial USB port
    """
    if sys.platform.startswith('win'):
        ports = ['COM{}'.format(n) for n in range(1, 256)]
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    elif sys.platform.startswith('linux'):
        ports = glob.glob('/dev/tty[A-Za-z]*')
    else:
        msg = '{} is not a supported platform'.format(sys.platform)
        raise EnvironmentError(msg)
    available_usb = list()
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            available_usb.append(port)
        except (OSError, serial.SerialException):
            pass
    return available_usb
