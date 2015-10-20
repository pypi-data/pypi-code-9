class WhaleException(Exception):
    pass


class ClientError(WhaleException):
    pass


class HttpTimeout(WhaleException):
    pass


class HttpBackoff(WhaleException):
    pass


class ApiError(WhaleException):
    pass


class ApiNotInitialized(WhaleException):
    pass
