import sys

from status import UNKNOWN, STATUS, OK
from exceptions import StatusNotExist, ParameterInvalid
from perf import PerformanceData


class NagiosPlugin(object):
    """ Nagios plugin

    """

    def __init__(self, name, print_header=True, print_perf=True):
        object.__init__(self)
        self._perf_data = []
        self._status = UNKNOWN
        self._name = name
        self._print_header = print_header
        self._print_perf = print_perf

    @property
    def status(self):
        return self._status

    # @status.setter
    # def status(self, value):
    #     if isinstance(value, int):
    #         if value not in range(0, 3+1):
    #             raise Exception("status accept only values 0, 1, 2, 3")
    #         else:
    #             self._status = value
    #     else:
    #         raise Exception("status muss be a int value")

    def start(self):
        try:
            self.main()
        except Exception as e:
            self.output(UNKNOWN, str(e))

    def main(self):
        self._status, msg_header, msg_perf = self.check()
        msg = "{} {}".format(self._name, STATUS[self.status].lower())
        if self._print_header and msg_header:
            msg += " " + msg_header
        if self._print_perf and msg_perf:
            msg += " | " + msg_perf
        self.output(self.status, msg)

    def add(self, perf_data):
        """ add a performance data

        :param perf_data: PerformanceData object
        :return: nothing
        """
        if not isinstance(perf_data, PerformanceData):
            raise ParameterInvalid("Input data isn't a PerformanceData object")
        self._perf_data.append(perf_data)

    def check(self):
        """ check status of all performance data

        :return: status
        :rtype: int
        """
        if len(self._perf_data) < 1:
            raise Exception("There aren't any data to check")
        status = OK
        msg = ""
        msg_perf = ""
        for perf_data in self._perf_data:
            if msg == "":
                msg = perf_data.str_result()
                msg_perf = perf_data.str_perf()
            else:
                msg += ", " + perf_data.str_result()
                msg_perf += " " + perf_data.str_perf()
            if perf_data.no_check:
                continue
            checked_status = perf_data.check()
            if checked_status > status:
                status = checked_status
            if status == UNKNOWN:
                break
        return status, msg, msg_perf

    @staticmethod
    def output(stt, msg):
        if isinstance(stt, int):
            status = stt
        elif isinstance(stt, str):
            if stt not in STATUS:
                raise StatusNotExist("Status: OK, WARNING, CRITICAL")
            status = STATUS[stt]
        else:
            raise StatusNotExist("Status: OK, WARNING, CRITICAL")
        if msg != '':
            sys.stdout.write("{}\n".format(msg))
        else:
            sys.stdout.write("{}\n".format(stt))
        sys.exit(status)
