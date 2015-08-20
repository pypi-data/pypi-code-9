# coding: utf-8


class ClientException(Exception):
    __slots__ = ('url', 'method', 'code', 'msg')

    def __init__(self, url, method, code, msg):
        self.url = url
        self.method = method
        self.code = code
        self.msg = msg

    def __str__(self):
        return 'Api error: {} {}({}): {}'.format(self.method, self.url, self.code, self.msg)

    def __unicode__(self):
        return u'Api error: {} {}({}): {}'.format(self.method, self.url, self.code, self.msg)


class UnauthorizedException(ClientException):
    pass


class ForbiddenException(ClientException):
    pass


class NotFoundException(ClientException):
    pass


class TooManyRequestsException(ClientException):
    pass


class PaymentRequiredException(ClientException):
    pass