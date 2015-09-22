from exceptions import ParameterInvalid, ValueInvalid
from status import OK, WARNING, CRITICAL


class PerformanceData(object):
    """ Nagios performance data
    """

    def __init__(self, name, value=None, warning=None, critical=None,
                 max_value='', min_value='', unit='', no_check=False,
                 type_check="asc"):
        """
        :param name: name of the performance data
        :param value: value
        :param warning: warning value
        :param critical: critical value
        :param max_value: max value to visualise
        :param min_value: min value to visualise
        :param unit: unit of the value
        :param no_check: True for ignore the result of this performance data
        :param type_check: 'asc' or 'desc', method to compare the value with
                           warning and critical values; default: 'asc'
        """
        object.__init__(self)
        if value is None:
            raise ParameterInvalid(
                "{} need a value".format(self.__class__.__name__))
        try:
            self.__value = int(value)
        except:
            raise ParameterInvalid("value invalid (only accept int or float)")
        self.type_check = type_check

        self.__name = name
        self.__warning = warning
        self.__critical = critical
        self.__max = max_value
        self.__min = min_value
        if unit != '' and unit not in ['s', 'us', 'ms', '%', 'B', 'KB', 'TB',
                                       'GB', 'c']:
            raise Exception("Unit invalid")
        self.__unit = unit
        self.e = None
        self.no_check = no_check

    @property
    def value(self):
        """ return value of the performance data (measuring)

        :return: value of the performance data (measuring)
        :rtype: float
        """
        return self.__value

    @value.setter
    def value(self, value):
        """ set the value of the performance data (measuring)

        :param value: value of the performance data (measuring)
        :type value: float
        """
        try:
            self.__value = float(value)
        except:
            raise ValueInvalid("value must be either int or float")

    def __repr__(self):
        """
        :return: performance data in string
        :rtype: str
        """
        return "{}={}{};{};{};{};{}".format(
            self.__name.strip().replace(' ', '_'), self.value,
            self.__unit if self.__unit is not None else '',
            self.__warning if self.__warning is not None else '',
            self.__critical if self.__critical is not None else '',
            self.__min if self.__min is not None else '',
            self.__max if self.__max is not None else '')

    def str_header(self):
        """ return the header of the result as string

        :return: header message
        :rtype: str
        """
        return "{} = {}{}".format(self.__name, self.value, self.__unit)

    def str_perf(self):
        """ return the performance data of the result as string

        :return: performance data
        :rtype: str
        """
        return self.__repr__()

    def check(self):
        """ check the performance data by comparing with warning and critical
        values
        :return: status code of this data/counter/gauge after checking
        :rtype: int
        """
        try:
            if self.type_check == "asc":
                if self.__critical is not None and self.__critical <= self.value:
                    return CRITICAL
                if self.__warning is not None and self.__warning <= self.value:
                    return WARNING
                return OK
            elif self.type_check == "desc":
                if self.__critical is not None and self.__critical >= self.value:
                    return CRITICAL
                if self.__warning is not None and self.__warning >= self.value:
                    return WARNING
                return OK
            else:
                return CRITICAL
        except:
            raise
