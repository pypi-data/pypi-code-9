
class RequestChannelNotExists(ValueError):
    pass


class ResponseChannelAlreadyExists(Exception):
    pass


class PackedRequestFail(ValueError):
    pass


class ResponseTimeOutError(Exception):
    pass


class UnpackedResponseFail(Exception):
    pass


class CallbackNotFound(ValueError):
    pass
