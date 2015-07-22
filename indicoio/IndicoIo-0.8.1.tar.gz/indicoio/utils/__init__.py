"""
Basic utility classes and functions
"""
import inspect

from indicoio.utils.errors import DataStructureException

class TypeCheck(object):
    """
    Decorator that performs a typecheck on the input to a function
    """
    def __init__(self, accepted_structures, arg_name):
        """
        When initialized, include list of accepted datatypes and the
        arg_name to enforce the check on. Can totally be daisy-chained.
        """
        self.accepted_structures = accepted_structures
        self.is_accepted = lambda x: type(x) in accepted_structures
        self.arg_name = arg_name

    def __call__(self, fn):
        def check_args(*args, **kwargs):
            arg_dict = dict(zip(inspect.getargspec(fn).args, args))
            full_args = dict(arg_dict.items() + kwargs.items())
            if not self.is_accepted(full_args[self.arg_name]):
                raise DataStructureException(
                    fn,
                    full_args[self.arg_name],
                    self.accepted_structures
                )
            return fn(*args, **kwargs)
        return check_args



def is_url(data, batch=False):
    if batch and isinstance(data[0], basestring):
        return True
    if not batch and isinstance(data, basestring):
        return True
    return False
