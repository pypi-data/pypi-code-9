"""
    flask.ext.keyauth
    ---------------

    This module provides RSA authentication and authorization for
    Flask. It lets you work with requests in a database-independent manner.

initiate the KeyManager with a app and set account ID, signature and timestamp
"""

from flask import current_app, request, abort
from functools import update_wrapper
import datetime
import urllib.parse
import json
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

#simple macros where x is a request object


class ArgsChecker(object):
    """
    This object is used to hold the settings for authenticating requests.  Instances of
    :class:`HmacManager` are not bound to specific apps, so you can create one in the
    main body of your code and then bind it to your app in a factory function.
    """
    def __init__(self, app=None):
        """
        :param app Flask application container
        """
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.args_checker = self

    def check(self, request_obj, required_args):
        for arg in required_args:
            try:
                request_obj.values.get(arg)
            except Exception as e:
                return False
        return True

def checkargs(args=None):
    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if current_app.args_checker.check(request, args):
                return f(*args, **kwargs)
            abort(403)
        return update_wrapper(wrapped_function, f)
    return decorator