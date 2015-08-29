# coding: utf-8
import exceptions

codes = {
    401: exceptions.UnauthorizedException,
    402: exceptions.PaymentRequiredException,
    403: exceptions.ForbiddenException,
    404: exceptions.NotFoundException,
    429: exceptions.TooManyRequestsException,
}
