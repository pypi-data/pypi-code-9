from flask import g
from functools import wraps


class Authorizator(object):

    def __init__(self, check_capability_func=None, authenticator=None):
        if check_capability_func:
            self.check_capability = check_capability_func
        self.authenticator = authenticator

    def check_capability(self, identity, capability):
        return NotImplemented()

    def identity_getter(self):
        return g.auth_identity

    def perform_authorization(self, capability):
        if not self.check_capability(self.identity_getter(), capability):
            raise CapabilityMissingException(capability)
        return True

    def requires_capability(self, capability):
        def decorator(f):
            @wraps(f)
            def decorated(*args, **kwargs):
                self.perform_authorization(capability)
                return f(*args, **kwargs)
            if self.authenticator:
                return self.authenticator.requires_authentication(decorated)
            return decorated
        return decorator


class CapabilityMissingException(Exception):

    def __init__(self, capability):
        Exception.__init__(self, capability)
