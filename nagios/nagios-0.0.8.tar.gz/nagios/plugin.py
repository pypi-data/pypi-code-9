import sys

from status import UNKNOWN, STATUS, OK
from exceptions import StatusNotExist, ParameterInvalid
from perf import PerformanceData


class NagiosPlugin(object):
    """ Nagios plugin object
    """

    def __init__(self, name, print_header=True, print_perf=True):
        """
        :param name: name of the plugin
        :param print_header: True for print header
        :param print_perf: True for print performance data
        """
        object.__init__(self)
        self._perf_data = []
        self._status = UNKNOWN
        self._name = name
        self._print_header = print_header
        self._print_perf = print_perf

    @property
    def status(self):
        return self._status

    def start(self):
        """ start the plugin automatic:
        - check all performance data
        - print result string
        - exit with status code

        if something go wrong, print the exception string and exit with status
        UNKNOWN
        """
        try:
            self.main()
        except Exception as e:
            self.output(UNKNOWN, str(e))

    def main(self):
        """ main function, will be call by starting
        """
        self._status, msg_header, msg_perf = self.check_all()
        msg = "{} {}".format(self._name, STATUS[self.status].upper())
        if self._print_header and msg_header:
            msg += ": " + msg_header
        if self._print_perf and msg_perf:
            msg += " | " + msg_perf
        self.output(self.status, msg)

    def add(self, perf_data):
        """ add a performance data into the plugin

        :param perf_data: PerformanceData object
        """
        if not isinstance(perf_data, PerformanceData):
            raise ParameterInvalid("Input data isn't a PerformanceData object")
        self._perf_data.append(perf_data)

    def check_all(self):
        """ check all performance data and return the summary status, message
        header, performance data message

        :return: (status, msg_header, msg_perf)
        :rtype: tuple
        """
        if len(self._perf_data) < 1:
            raise Exception("There aren't any data to check")
        status = OK
        msg_header = ""
        msg_perf = ""
        for perf_data in self._perf_data:
            if msg_header:
                msg_header += ", "
                msg_perf += " "

            msg_header += perf_data.str_header()
            msg_perf += perf_data.str_perf()

            if perf_data.no_check:
                continue
            checked_status = perf_data.check()
            if checked_status > status:
                status = checked_status
        return status, msg_header, msg_perf

    @staticmethod
    def output(stt, msg):
        """ print message (msg) and exit with status code of stt

        :param stt: status id or status str
        :param msg: message to show
        """
        if isinstance(stt, int):
            status = stt
        elif isinstance(stt, str):
            if stt not in STATUS:
                raise StatusNotExist()
            status = STATUS[stt]
        else:
            raise StatusNotExist()
        sys.stdout.write("{}\n".format(msg))
        sys.exit(status)
