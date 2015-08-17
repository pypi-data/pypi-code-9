""" logging and convenience functions for Phidgets relays.

Usage:
    rel = Relay()
    rel.zero_on()
    rel.two_toggle()
    
All connections are made and closed during the operations for that
relay. The connection is not kept open.
"""

import logging

from Phidgets.PhidgetException import PhidgetException
from Phidgets.Devices.InterfaceKit import InterfaceKit

class Relay(object):
    """ Relay class wraps language around the 1014_2 -
    PhidgetInterfaceKit 0/0/4 4 relay device. Also works for
    SSR relays."""

    def __init__(self, in_serial=None):

        # http://victorlin.me/posts/2012/08/26/\
        # good-logging-practice-in-python
        self.log = logging.getLogger(__name__)
        if in_serial != None:
            # On odroid C1, int conversion raises null byte in argument
            # strip out the null byte first
            in_serial = in_serial.strip('\0')
            self._serial = int(in_serial)
        else:
            self._serial = None
        self.log.debug("Start of phidgeter with serial: %s" % in_serial)


    def change_relay(self, relay=0, status=0):
        """ Toggle the status of the phidget relay line to low(0) or 
        high(1) status
        """
        self.interface.setOutputState(relay, status)
        return 1

    def open_phidget(self):
        self.log.debug("Attempting to open phidget")

        self.interface = InterfaceKit()

        if self._serial != None:
            self.log.debug("Attempt to open serial: %s" % self._serial)
            self.interface.openPhidget(self._serial)
        else:
            self.log.debug("Attempt to open first found")
            self.interface.openPhidget()

        wait_interval = 300
        self.log.debug("Wait for attach %sms" % wait_interval)           
        self.interface.waitForAttach(wait_interval)
  
        self.log.info("Opened phidget") 
        return 1

    def close_phidget(self):
        self.log.debug("Attempting to close phidget")
        self.interface.closePhidget()
        self.log.info("Closed phidget") 
        return 1

        

    def open_operate_close(self, relay, status): 
        """ Open the phidget, change the relay to status, close phidget.
        """
        self.open_phidget()
        result = self.change_relay(relay, status)
        self.close_phidget()
        return result

    def open_toggle_close(self, relay):
        """ Find the current status of the specified relay, and set the
        status to the opposite.
        """
        self.open_phidget()
        curr_state = self.interface.getOutputState(relay)
        result = self.change_relay(relay, not curr_state)
        self.close_phidget()
        return result

    def zero_on(self):
        return self.open_operate_close(relay=0, status=1)

    def zero_off(self):
        return self.open_operate_close(relay=0, status=0)

    def zero_toggle(self):
        return self.open_toggle_close(relay=0)

    def one_on(self):
        return self.open_operate_close(relay=1, status=1)

    def one_off(self):
        return self.open_operate_close(relay=1, status=0)

    def one_toggle(self):
        return self.open_toggle_close(relay=1)

    def two_on(self):
        return self.open_operate_close(relay=2, status=1)

    def two_off(self):
        return self.open_operate_close(relay=2, status=0)

    def two_toggle(self):
        return self.open_toggle_close(relay=2)

    def three_on(self):
        return self.open_operate_close(relay=3, status=1)

    def three_off(self):
        return self.open_operate_close(relay=3, status=0)

    def three_toggle(self):
        return self.open_toggle_close(relay=3)
