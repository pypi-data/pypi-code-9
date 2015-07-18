class GnipException(Exception):
    pass


class GnipUnauthorizedException(GnipException):
    """
    Gnip API Returned 401 Unauthorized
    HTTP authentication failure due to invalid credentials
    """
    pass


class GnipRulesFormatError(GnipException):
    """
    Invalid Rules Format
    """
