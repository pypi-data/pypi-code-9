class Error(Exception):
    """Base error for all custom errors this package can raise."""


class APIError(Error):
    """Raised when an error is received in an API response.

    :param code: internal error code
    :param message: error message in response
    """

    def __init__(self, code, message):
        self.code = code
        self.message = message

    def __str__(self):
        return '[{0}] {1}'.format(self.code, self.message)

    def __repr__(self):
        return '{0}({1!r}, {2!r})'.format(self.__class__.__name__, self.code, self.message)


class ValidationError(Error):
    """Raised when input is not valid."""
