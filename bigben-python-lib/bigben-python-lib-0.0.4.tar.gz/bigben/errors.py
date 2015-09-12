
"""
    Errors used by the BigBen Client Library.
"""


class BigBenError(Exception):
    """
        Parent class of all all errors raised by this library.
    """

    def __init__(self, message):
        """
            Initializes a BigBenError.

            Args:
                message: A user-friendly error message, , as a StringType
        """
        self.message = message


class BigBenHttpError(BigBenError):
    """
        Error indicating that the API has returned a non-successful response.
    """

    def __init__(self, http_code, error_code, message = None):
        """
            Initializes a BigBenHttpError.

            Args:
                http_code: The HTTP status code number that was returned, as an IntType
                error_code: The BigBen error code used indicating more specific
                    error cases, as an IntType
                message: A user-friendly error message.  If one is not provided,
                    a default message will be used, as a StringType
        """
        if message is None:
            message = 'Http Request failed with HTTP status code: %s' % http_code
        super(BigBenHttpError, self).__init__(message)

        self.http_code = http_code
        self.error_code = error_code
        self.message = message

    def __str__(self):
        """
            Returns a user friendly representation of this error.
        """

        return "HttpCode: %s, ErrorCode: %s, Message: %s" % (self.http_code,
                                                             self.error_code,
                                                             self.message)
