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


def prompt_available_usb():
    """
        Prompt in console the choice between the available usb port
        if only one is found, return it.
        If there is no available port, return None

    :return: str
    """
    available_usb = get_available_usb()
    if not available_usb:
        return None
    if len(available_usb) == 1:
        return available_usb[0]
    print 'Available port:'
    for i in range(len(available_usb)):
        print '\t{}. {}'.format(i + 1, available_usb[i])
    choice = 0
    correct_input = False
    while not correct_input:
        try:
            choice = int(raw_input('Choose the UBS port: ')) - 1
            if choice in range(0, len(available_usb)):
                correct_input = True
        except ValueError:
            pass
    return available_usb[choice]
