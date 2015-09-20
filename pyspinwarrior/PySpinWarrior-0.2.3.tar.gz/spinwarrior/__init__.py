"""PySpinWarrior - Interacting with Spin Warrior devices from Python"""

from __future__ import print_function
import sys
import logging
import ctypes
import time

__version__ = '0.2.3'

logger = logging.getLogger('spinwarrior')

# Constants from spinkit.h
SPINKIT_VENDOR_ID = 0x07C0
SPINKIT_PRODUCT_ID24R4 = 0x1200
SPINKIT_PRODUCT_ID24R6 = 0x1201
SPINKIT_PRODUCT_ID24A3 = 0x1202
SPINKIT_MAX_DEVICES = 16

Nspins = 6
Nbuttons = 7

# Load the library
try:
    if 'win' in sys.platform:
        clib = ctypes.WinDLL('spinkit.dll')
    else:
        clib = ctypes.CDLL('./libspinkit.so')
    online = True
except OSError as e:
    logger.error('Unable to load shared library. Is it installed?')
    logger.warn('Proceeding in offline mode. Results will be simulated.')
    online = False


class SpinWarriorError(Exception):
    """Standard exception for errors associated with the Spin Warrior
    SDK.

    """


class SpinKitData(ctypes.Structure):
    """Imported struct from spinkit.h."""
    _fields_ = [
        ('Device', ctypes.c_void_p),
        ('Spins', ctypes.c_int*Nspins),
        ('Buttons', ctypes.c_int*Nbuttons)
    ]

    def pythonize(self):
        """Pythonize the SpinKitData by converting to a dict."""
        pydata = {}
        pydata['spins'] = [self.Spins[i] for i in range(Nspins)]
        pydata['buttons'] = [self.Buttons[i] for i in range(Nbuttons)]
        return pydata

    @classmethod
    def null_pythonize(self):
        """Same as the :meth:`pythonize` function, but for when there
        is no new data.

        """
        return {'spins': [0]*6, 'buttons': [0]*7}


class SpinWarrior(object):
    """Class for interacting with SpinWarrior devices."""
    def __init__(self, handle=None):
        """Open a SpinWarrior device.

        Parameters
        ----------
        handle : int or None
            If None, opens all SpinWarrior devices found, but only
            represents the first found. If a handle is given, a
            specific SpinWarrior device will be addressed.
        online : bool
            If False, simulate an attached device.

        """
        # Open device
        assert isinstance(handle, int) or handle is None
        if online:
            dev = clib.SpinKitOpenDevice()
            logger.debug("Device handle: " + str(dev))
        else:
            dev = 1
            logger.debug("Simulating device with handle 1")
        if not dev:
            raise SpinWarriorError("Error opening Spin Warrior device.")
        if handle is None:
            self._dev = dev
        else:
            num_devs = clib.SpinKitGetNumDevs()
            if handle <= 0 or handle > num_devs:
                raise SpinWarriorError(
                    "Invalid device number. Must be between 1 and {}".format(num_devs))
            dev = clib.SpinKitGetDeviceHandle(handle)
            if not dev:
                raise SpinWarriorError(
                    "Error opening device number " + str(handle))
            self._dev = dev

        sertype = ctypes.c_wchar*9
        serialnumber = sertype()
        clib.SpinKitGetSerialNumber(self._dev, ctypes.byref(serialnumber))
        self._serial = serialnumber.value
        self._revision = clib.SpinKitGetRevision(self._dev)
        self._product_id = clib.SpinKitGetProductId(self._dev)
        version = ctypes.c_char_p(clib.SpinKitVersion())
        self._spinkit_version = version.value

    def __enter__(self):
        return self

    def __exit__(self, t, v, tb):
        self.close()

    def close(self):
        """Safely close the device."""
        if online:
            clib.SpinKitCloseDevice(self._dev)

    def read(self, wait=False, timeout=1000):
        """Read from the device. This does not block, so if nothing
        changes, all data should be 0.

        TODO: Generate random data if not online

        Parameters
        ----------
        wait : bool
            When True, use the blocking read call.
        timeout : int
            Time in ms to wait for blocking reads.

        """
        data = SpinKitData()
        assert isinstance(wait, (bool, int))
        assert isinstance(timeout, int)
        if online:
            if wait:
                clib.SpinKitSetTimeout(self._dev, timeout)
                res = clib.SpinKitRead(self._dev, ctypes.byref(data))
            else:
                res = clib.SpinKitReadNonBlocking(
                    self._dev, ctypes.byref(data))
        else:
            res = True
        if res:
            return data.pythonize()
        else:
            # No new data
            return SpinKitData.null_pythonize()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    with SpinWarrior() as dev:
        print("Device serial", dev._serial)
        print("Device revision", hex(dev._revision))
        print("Product ID", hex(dev._product_id))
        print(dev._spinkit_version)
        left = 0
        right = 0
        while True:
            data = dev.read(wait=True, timeout=2000)
            print(data)
            time.sleep(0.05)
