from .util import ApiXmlHelper


class KempTechApiException(Exception):
    """Raised if HTTP request has failed."""

    def __init__(self, msg=None, code=None, is_xml_msg=True):
        if msg is not None:
            # 400 Errors should be handled here. This will pass the error
            # message given by the LoadMaster API and show it as the exception
            # message in the traceback.
            message = ApiXmlHelper.get_error_msg(msg) if is_xml_msg else msg
        else:
            # 400+ shouldn't be handled here, but cover it anyway.
            # This is just optional fallback for
            # laziness when no message is given.
            if code == 400:
                message = "400 Mandatory parameter missing from request."
            elif code == 401:
                message = "401 Client Error: Authorization required."
            elif code == 403:
                message = "403 Incorrect permissions."
            elif code == 404:
                message = ("404 Not found. "
                           "Ensure the API is enabled on the LoadMaster.")
            elif code == 405:
                message = "405 Unknown command."
            else:
                message = "An unknown error has occurred."
        super(KempTechApiException, self).__init__(message)


class KempConnectionError(KempTechApiException):
    def __init__(self, endpoint):
        msg = "A connection error occurred to {endpoint}."\
            .format(endpoint=endpoint)
        super(KempConnectionError, self).__init__(msg)


class UrlRequiredError(KempTechApiException):
    def __init__(self, cmd_url):
        msg = "{} is an invalid URL".format(cmd_url)
        super(UrlRequiredError, self).__init__(msg)


class TooManyRedirectsException(KempTechApiException):
    def __init__(self, cmd_url):
        msg = "Too many redirects with request to {}.".format(cmd_url)
        super(TooManyRedirectsException, self).__init__(msg)


class TimeoutException(KempTechApiException):
    def __init__(self, endpoint):
        msg = "A connection {} has timed out.".format(endpoint)
        super(TimeoutException, self).__init__(msg)


class HTTPError(KempTechApiException):
    def __init__(self, cmd_url):
        msg = "A HTTP error occurred with request to {}.".format(cmd_url)
        super(HTTPError, self).__init__(msg)


class ApiNotEnabledError(KempTechApiException):
    def __init__(self):
        msg = "Ensure the API is enabled on the LoadMaster."
        super(ApiNotEnabledError, self).__init__(msg)


class CommandNotAvailableException(KempTechApiException):
    def __init__(self, cmd_name):
        msg = "Command '{}' is not available on the LoadMaster.".format(cmd_name)
        super(CommandNotAvailableException, self).__init__(msg, is_xml_msg=False)
