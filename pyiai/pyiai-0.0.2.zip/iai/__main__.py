from time import sleep
from iai.Controller import Controller
from iai.Axis import SSELAxis
from iai.DigitalIO import DigitalIO


def self_test():
    controller = Controller("COM5", 9600, 5)
    out = DigitalIO(controller, 323)
    for i in range(10):
        out.set(1)
        sleep(0.3)
        out.set(0)
        sleep(0.3)



if __name__ == "__main__":
    self_test()
