__author__ = 'mkoponen'

from finch_urllib2.errors import HTTPError

# Intrazon-specific errors start from 1000 up. Otherwise they are HTTP error codes, except for special case 599 which
# means timeout


intrazon_error_codes = {
    1000: "Unknown error",
    1001: 'Wrong class to callback',
}


class IntraZonError(Exception):
    def __init__(self, code):
        self.code = code
        if code >= 1000:
            message = intrazon_error_codes[code]
        else:
            finch_http_error = HTTPError(code)
            message = finch_http_error.message
        super(IntraZonError, self).__init__(message)
