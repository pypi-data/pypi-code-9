
class ServiceException(Exception):
    pass


class CommandError(ServiceException):
    pass


class DisconnectedError(ServiceException):
    pass


class AuthFailedError(ServiceException):
    pass


class RPCError(ServiceException):
    pass


class ConfigurationException(ServiceException):
    pass