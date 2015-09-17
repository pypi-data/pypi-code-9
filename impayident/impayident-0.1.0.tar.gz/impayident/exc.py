
from prettyexc import PrettyException as Exception


class ImpayException(Exception):
    pass


class HttpException(ImpayException):
    pass


class ApiException(ImpayException):
    pass
