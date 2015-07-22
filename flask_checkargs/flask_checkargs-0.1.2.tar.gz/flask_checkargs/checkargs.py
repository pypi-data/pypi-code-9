"""
    flask.ext.checkargs
    ---------------

    This module provides a way to check if all the required arguments are in the incoming request.

"""

from flask import current_app, request, abort
from functools import update_wrapper


class CheckArgs(object):
    def __init__(self, app=None):
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

def check_args(args=None):
    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if current_app.args_checker.check(request, args):
                return f(*args, **kwargs)
            abort(403)
        return update_wrapper(wrapped_function, f)
    return decorator