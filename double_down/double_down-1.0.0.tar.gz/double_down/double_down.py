from functools import wraps


def double_down(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        """ Simply prepend the function call with... another function call """
        f(*args, **kwargs)
        return f(*args, **kwargs)

    return wrapped
