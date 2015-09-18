from exceptions import ParameterInvalid, ValueInvalid
from status import OK, WARNING, CRITICAL


class PerformanceData(object):
    """ Nagios performance data
    """

    def __init__(self, name, value=None, warning=None, critical=None,
                 max_value='', min_value='', unit='', no_check=False,
                 type_check=None):
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
        return self.__value

    @value.setter
    def value(self, value):
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
            self.__unit, self.__warning,
            self.__critical, self.__min,
            self.__max)

    def str_result(self):
        return "{} = {}{}".format(self.__name, self.value, self.__unit)

    def str_perf(self):
        return self.__repr__()

    def check(self):
        """
        :return: status of this data/counter/gauge after checking
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
