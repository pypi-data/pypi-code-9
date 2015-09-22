from .status import STATUS


class ValueInvalid(Exception):
    pass


class ParameterInvalid(Exception):
    pass


class StatusNotExist(Exception):
    def __init__(self):
        super(StatusNotExist, self).__init__(
            "Only accept status " + str([stt for stt in STATUS]))
