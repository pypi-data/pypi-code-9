from obdlib.obd.pids import *

# OBD Modes (described in OBD-II standard SAE J1979)
CURRENT_DATA = 1
FREEZE_FRAME_DATA = 2
REQUEST_TROUBLE_CODES = 3
CLEAR_TROUBLE_CODES_AND_VALUES = "04"
OXYGEN_SENSOR_DATA = "05"
SYSTEM_MONITORING_DATA = "06"
PENDING_TROUBLE_CODES = "07"
CONTROL_OPERATION = "08"
VEHICLE_INFORMATION_DATA = 9
PERMANENT_TROUBLE_CODES = "0A"

DEFAULT_OBD_MODE = CURRENT_DATA


class DictModes(dict):
    pids = None

    def __getitem__(self, key):
        """
            Override the base getitem method,
            because we need to set a mode before
            retrieves value of dict
        """
        # sets current mode
        DictModes.pids.set_mode(key)
        val = dict.__getitem__(self, key)
        return val


class Modes(object):
    """
        Provides list of OBD modes
    """
    __slots__ = ['modes']

    def __init__(self, units):
        set_unit(units)
        # In order to choose right pid you
        # need to do next request (ex: get engine coolant temperature -
        # self.modes[1][5])
        DictModes.pids = Pids()
        pre_dict = {
            # Current data - 01
            CURRENT_DATA: DictModes.pids,
            # Trouble codes
            REQUEST_TROUBLE_CODES: DictModes.pids,
            # Common info
            VEHICLE_INFORMATION_DATA: DictModes.pids
        }
        self.modes = DictModes(pre_dict)