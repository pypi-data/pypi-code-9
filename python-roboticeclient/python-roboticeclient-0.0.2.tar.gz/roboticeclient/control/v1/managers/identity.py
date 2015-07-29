
import sys
import six
import json
import logging

from . import base

LOG = logging.getLogger("users")

from .users import UserManager
from .auth import AuthManager


class IdentityManager(base.BaseManager):

    SCOPE = "identity"

    # PROXY
    users = UserManager()
    auth = AuthManager()

    def switch_location(self, request, data):
        return self.request(
            request,
            '/{0}/location/switch/'.format(self.SCOPE),
            'POST',
            data)