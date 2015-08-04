from obdlib.elm327 import NO_RESULT
from obdlib.obd.modes import Modes
from obdlib.logging import logger


class Command(object):
    """
        This class to provide the common functionality
        to make PID's request
    """

    def __init__(self, call_obd, units):
        """
            Init the common params
            :param call_obd: request function
            :param units: flag of conversion (0 - Europe, 1 - English,
            ex: km/h - > mph)
        """
        self.__modes = Modes(units)
        self.__call = call_obd
        self.__decoder = lambda: None
        self.title = None
        self.description = None
        self.pid = None
        self.bytes = None
        self.value = None
        self.unit = None
        self.kwargs = None
        # list of pids (available or not)
        self.__pids = {}
        self.__ecus = {}

    def init(self, args):
        """
            Unpacks modes params
            :param args - mode params
        """
        self.title, self.description, self.pid, \
        self.bytes, self.unit, self.__decoder, self.kwargs = args

    @property
    def ecus(self):
        """
            Generates available ECU's value
            :return tuple (ecu, value)
        """
        for ecu, value in self.__ecus.items():
            yield (ecu, value)

    def sensors(self, mode=1):
        """
            Generates available ECU's and PID's value
        """
        for ecu, pids in self.__pids.items():
            for pid, access in pids.items():
                if self.is_not_access(access, pid):
                    continue
                self[mode](pid)
                yield self

    def is_not_access(self, access, pid):
        return not access or int(pid, 16) in (0, 32, 64,)

    def check_pids(self):
        """
            Checks available PIDs. If return data, it means connected True
            Prepares the ELM327 for communicating with vehicle - 01 pid 00
        """
        self.__pids = {}
        pids = self[1]('00')  # 01 00
        if self.is_ecus(pids):
            self.__pids.update(pids.__ecus)
            self.add_pids()
            return True

    def add_pids(self):
        for ecu in self.__pids.keys():
            if self.__pids[ecu].get('20'):  # add 21-40 pids if available
                self.__pids[ecu].update(self[1]('20').__ecus[ecu])
            if self.__pids[ecu].get('40'):  # add 41-60 pids if available
                self.__pids[ecu].update(self[1]('40').__ecus[ecu])

    def is_ecus(self, pids):
        return pids and isinstance(pids.__ecus, dict) and len(pids.__ecus)

    def is_pids(self, check=True):
        """
            Returns True, if some of the PID's are available
        """
        resp = False
        for ecu, pids in self.__pids.items():
            items = pids.values()
            if isinstance(check, str):
                # for check pids
                items = pids.keys()
            if check in items:
                resp = True
                break
        return resp

    def _set_value(self, value):
        """
            Converts (if needed) and sets current value of sensor
        """
        if NO_RESULT != value and value is not None:
            value = self.__decoder(
                value,
                **self.kwargs) if self.kwargs else self.__decoder(value)

        return value

    def _process(self):
        """
            Decodes OBD data
        """
        return dict(
            [k, self._set_value(v)]
            for k, v in self.__call(self.pid).value.items()
        )

    def _process_pid(self, mode, pid):
        if not isinstance(pid, str):
            raise Exception("PID {} must be a string.".format(pid))

        # checks unsupported PIDs
        if self._is_supported(pid):
            raise Exception(
                "Unsupported command. {} PID {}".format(
                    mode,
                    pid))

        pid = int(pid, 16)
        pid_info = self.__modes.modes[mode][pid]

        if not pid_info:
            # if command does not describe in the modes class
            raise Exception(
                "Unsupported command. {} PID {}".format(
                    mode,
                    pid))

        self.init(pid_info)
        self.__ecus.update(self._process())

    def _is_supported(self, pid):
        """
            Checks an available PID
        """
        return pid != '00' and not self.is_pids(pid)

    def __getitem__(self, mode):
        self.__ecus = {}

        def get_pid(pid='00'):
            try:
                self._process_pid(mode, pid)
            except Exception as err:
                # logging
                logger.error(err)
            return self

        return get_pid
