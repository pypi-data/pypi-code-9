from functools import wraps
from fabric.api import *
from fabric.api import task as _task

def fix_boolean(f):
    """ each argument passed to f is 'booleanized', if a string 'false' or 'true' is found, it will make them bool
    """
    def fix_bool(value):
        if isinstance(value, basestring):
            if value.lower() == 'false':
                return False
            if value.lower() == 'true':
                return True
        return value

    @wraps(f)
    def wrapper(*args, **kwargs):
        args_ = [fix_bool(arg) for arg in args]
        kwargs_ = {k: fix_bool(v) for k,v in kwargs.iteritems()}
        return f(*args_, **kwargs_)

    return wrapper

def task(f):
    """ fabric task - where strings 'false'/'true' are passed as boolean False/True instead.

    fabric does not sanitizes bool strings, e.g. fab deploy:config=False will pass 'False' instead of False
    (and 'False' evaluates to True, so that is a problem)
    """
    return _task(fix_boolean(f))

