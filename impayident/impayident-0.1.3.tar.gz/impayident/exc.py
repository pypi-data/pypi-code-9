
from prettyexc import PrettyException as Exception


class ImpayException(Exception):
    pass


class ArgumentException(ImpayException):
    pass


class HttpException(ImpayException):
    pass


class ApiException(ImpayException):
    pass
