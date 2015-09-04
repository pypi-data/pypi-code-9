# -*- coding: utf-8 -*-
from __future__ import absolute_import
import json
import logging
from functools import update_wrapper

from parse import parse

from flask import Response

class APIException(Exception):
    message_format = "Undefined"

class MissingParameterException(APIException):
    message_format = "Missing parameter: {}"
    def __init__(self, message):
        APIException.__init__(self, self.message_format.format(message))

class InvalidParameterException(APIException):
    message_format = "Invalid parameter: {}"
    def __init__(self, message):
        APIException.__init__(self, self.message_format.format(message))

class InvalidCredentialsException(APIException):
    message_format = "Invalid authentication credentials"
    def __init__(self, message=None):
        APIException.__init__(self, self.message_format.format(message))

class NotAuthedException(APIException):
    message_format = "User not authorized: {}"
    def __init__(self, message=None):
        APIException.__init__(self, self.message_format.format(message))

class PermissionDeniedException(APIException):
    message_format = "You do not have permission to use {}"
    def __init__(self, message):
        APIException.__init__(self, self.message_format.format(message))

class DataServiceNotFoundException(APIException):
    message_format = "Data service not found: service {}, version {}"
    def __init__(self, service, version):
        APIException.__init__(self, self.message_format.format(service, version))

class UnsupportedVersionException(APIException):
    message_format = "Unsupported version: {}"
    def __init__(self, version):
        APIException.__init__(self, self.message_format.format(version))

class UnsupportedMethodException(APIException):
    message_format = "Unsupported method: {}"
    def __init__(self, method):
        APIException.__init__(self, self.message_format.format(method))

class MalformedResponseException(APIException):
    message_format = "The response from the data service was malformed: {}"
    def __init__(self, response):
        APIException.__init__(self, self.message_format.format(response))

class VersionMismatchException(APIException):
    message_format = "The version code between the client ({}) and the data service ({}) don't match"
    def __init__(self, client_version, service_version):
        APIException.__init__(self, self.message_format.format(client_version, service_version))

class RateLimitExceededException(APIException):
    message_format = "You have exceeded the rate limit"
    def __init__(self):
        APIException.__init__(self, self.message_format)

class QueryTooLargeException(APIException):
    message_format = "Your query asks for too much data. You can only request a maximum of {} per query."
    def __init__(self, maximum):
        APIException.__init__(self, self.message_format.format(maximum))

class TestErrorException(APIException):
    message_format = "This is a test error. Message: {}"
    def __init__(self, message=None):
        APIException.__init__(self, self.message_format.format(message))

class UnknownErrorException(APIException):
    message_format = "{}"
    def __init__(self, message):
        APIException.__init__(self, self.message_format.format(message))

CODE_MAP = {
    'missing_parameter': MissingParameterException,
    'invalid_parameter': InvalidParameterException,
    'invalid_credentials': InvalidCredentialsException,
    'not_authed': NotAuthedException,
    'permission_denied': PermissionDeniedException,
    'data_service_not_found': DataServiceNotFoundException,
    'unsupported_version': UnsupportedVersionException,
    'unsupported_method': UnsupportedMethodException,
    'malformed_response': MalformedResponseException,
    'version_mismatch': VersionMismatchException,
    'rate_limit_exceeded': RateLimitExceededException,
    'query_too_large': QueryTooLargeException,
    'test_error': TestErrorException,
    'unknown_error': UnknownErrorException
}

def get_exception(code):
    return CODE_MAP.get(code)

def get_code(exception):
    exception_class = type(exception)
    if issubclass(exception_class, APIException):
        for key, value in CODE_MAP.items():
            if exception_class == value:
                return key

    return None

def make_exception_from_code_and_message(code, message):
    exception_class = get_exception(code)
    if exception_class is None:
        return UnknownErrorException("code: {}, message: {}".format(code, message))

    args = list(parse(exception_class.message_format, message))

    return exception_class(*args)


def make_error(code, message):
    return Response(json.dumps({"status": "error", "code": code, "message": message}), mimetype="application/json")

def make_error_restful(code, message):
    return {"status": "error", "code": code, "message": message}, 400

### Flask exception wrappers ###
def catch_exceptions(func):
    def catch_and_call(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.exception(func.__name__ + " failed")

            code = get_code(e) or "unknown_error"

            message = type(e).__name__ + ": " + e.__str__() if code == "unknown_error" else e.__str__()

            return make_error(code, message)
    return update_wrapper(catch_and_call, func)

def catch_exceptions_restful(func):
    def catch_and_call(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.exception(func.__name__ + " failed")

            code = get_code(e) or "unknown_error"

            message = type(e).__name__ + ": " + e.__str__() if code == "unknown_error" else e.__str__()

            return make_error_restful(code, message)
    return update_wrapper(catch_and_call, func)
