import logging

""" used o define the customize exception

    Internal exceptions that can be generated in network interface code.
These are use to control what the upper levels should do when different
types of errors occur.
"""

_logger = logging.getLogger(__name__)


class ConfigurationError(Exception):
    pass


class NetworkInterfaceException(Exception):
    pass


class ForceAgentRestart(NetworkInterfaceException):
    pass


class ForceAgentDisconnect(NetworkInterfaceException):
    pass


class DiscardDataForRequest(NetworkInterfaceException):
    pass


class RetryDataForRequest(NetworkInterfaceException):
    pass


class ServerIsUnavailable(RetryDataForRequest):
    pass


class InvalidLicenseException(NetworkInterfaceException):
    pass


class InvalidDataTokenException(NetworkInterfaceException):
    pass


class OutOfDateConfigException(NetworkInterfaceException):
    pass
