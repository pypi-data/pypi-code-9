""" This module contains decorator generators.
    Essentially this will be a medley of delicious functions
    to generate relatively useful, reusable, generic decorators for code.
"""

def function_registrator(target):
    """ function_registrator generates a simple decorator that will
        take a function with any set of arguments and register that
        function within a target list.
    """

    def decorator(func):
        """ This is a "flexible" decorator function that pushes to
            target thanks to scope magic.
        """

        if func not in target:
            target.append(func)

        return func

    return decorator


def function_marker(attr, value):
    """ function marker generates a simple decorator that will
        take a function with any set of arguments and set a given
        attribute on that function with setattr().
    """

    def decorator(func):
        """ This is a "flexible" decorator function that sets the
            attribute on the target function.
        """

        setattr(func, attr, value)

        return func

    return decorator

