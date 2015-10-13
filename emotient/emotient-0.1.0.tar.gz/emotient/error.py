def format_error_message(json_content):
    if 'validation_errors' in json_content:
        error_msg = u'{} - {}'.format(json_content['message'].rstrip('.'), json_content['validation_errors'])
    elif 'parameters' in json_content:
        error_msg = u'{} - {}'.format(json_content['message'].rstrip('.'), json_content['parameters'])
    else:
        error_msg = json_content['message']

    return error_msg


def get_error(status_code):
    return ERRORS.get(status_code, EmotientAPIError)


class EmotientAPIError(Exception):
    default_message = ''

    def __init__(self, message=None, status_code=None, http_content=None):
        self.message = message or self.default_message
        super(EmotientAPIError, self).__init__(message)
        self.status_code = status_code
        self.http_content = http_content


class NotAuthenticated(EmotientAPIError):
    pass


class MalformedRequest(EmotientAPIError):
    pass


class NotFound(EmotientAPIError):
    pass


class PermissionDenied(EmotientAPIError):
    pass


class Conflict(EmotientAPIError):
    pass


class Gone(EmotientAPIError):
    pass


ERRORS = {
    400: MalformedRequest,
    401: NotAuthenticated,
    403: PermissionDenied,
    404: NotFound,
    409: Conflict,
    410: Gone
}
