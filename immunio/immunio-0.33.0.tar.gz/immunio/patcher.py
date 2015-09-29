from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import functools
import inspect
import sys


# Global store of all current monkeypatches. Used by `unwrap_all()` to remove
# all patching.
_PATCHES = {}


def unwrap_all():
    """
    Unwrap all monkeypatching done with the `@monkeypatch()` decorator.
    """
    global _PATCHES

    # Loop through ever patch and unwrap it. Converted to a list since doing
    # the unpatching will mutate the `_PATCHES` dict.
    for _, wrapped in list(_PATCHES.items()):
        wrapped.immunio_unwrap()


def monkeypatch(target_or_base, target=None):
    """
    Monkeypatch the specified target with the decorated function.

    If only one argument is provided, it must be a string referencing the
    function to monkey patch.

    If two arguments are specified, the first must be a module or class,
    and the second must be a string referencing the attribute to be
    monkey patched.

    Example usage:

    class SomeClass(object):
        def some_method(self, a, b, c):
            pass

    To wrap `some_method()` above, you use monkeypatch like this when
    defining a wrapped function:

    @monkeypatch(SomeClass, "some_method")
    def _my_version(orig, self, a, b, c):
        # Here, self, a, b, c are the exact arguments that would have been
        # passed to the original `some_method()`. `orig` is a reference to
        # the original unwrapped version of the mthod. This allows you to
        # call the original version of the method.

        return orig(self, a, b, c)

    """
    global _PATCHES

    # Validate we have the correct number and type of arguments
    if target is None and not isinstance(target_or_base, basestring):
        raise ValueError("Invalid arguments to monkeypatch()")
    if target is not None and not isinstance(target, basestring):
        raise ValueError("Invalid arguments to monkeypatch()")

    # If the first argument is a string, resolve the base and target from there.
    if isinstance(target_or_base, basestring):
        parts = target_or_base.split(".")
        base = sys.modules[parts[0]]

        for part in parts[1:-1]:
            base = getattr(base, part)
        target = parts[-1]
    else:
        # If the first argument is not a string, it IS the base.
        base = target_or_base

    # Ensure base is a module or class - we don't support patching instances yet
    if not inspect.ismodule(base) and not inspect.isclass(base):
        raise NotImplementedError(
            "Base must be a module or class. "
            "Patching instances is not currently supported.")

    def wrapper(wrapped):
        """
        This `wrapper` function is called with the new function as it's single
        argument.
        """
        # Get a reference to the original version of the function we're wrapping
        original = getattr(base, target)

        # Determine what type of function/method we're wrapping
        is_bare_function = inspect.isfunction(original)
        is_classmethod = (
            inspect.ismethod(original) and original.__self__ is base)
        is_staticmethod = is_bare_function and inspect.isclass(base)

        # For classmethods, we need to access the underlying bare function.
        # This allows `orig()` to be called with the class as the first argument
        # in the same way as wrapped instance methods.
        if is_classmethod:
            original = original.__func__

        # If we're already wrapped the original before, don't double-wrap it,
        # wrap the original version instead.
        if hasattr(original, "_immunio_original"):
            original = original._immunio_original

        # Define the new replacement function. The replacement just calls
        # the decorated function with the additional `orig` argument.
        @functools.wraps(original)
        def new_wrapped(*args, **kwargs):
            return wrapped(original, *args, **kwargs)

        # Add the `_immunio_original` function attribute so we keep a reference
        # to the unwrapped version of the function.
        setattr(new_wrapped, "_immunio_original", original)

        def unwrap():
            """
            Remove the Immunio wrapping from this function.
            """
            orig = getattr(base, target)._immunio_original
            # Remove the reference from the global patches dict
            del _PATCHES[orig]
            # Add back the required decorators
            if is_classmethod:
                orig = classmethod(orig)
            elif is_staticmethod:
                orig = staticmethod(orig)
            setattr(base, target, orig)

        # Add an `immunio_unwrap()` attribute to the wrapped function to allow
        # our wrapping to be "undone".
        setattr(new_wrapped, "immunio_unwrap", unwrap)
        # Save a reference to this wrapped function so we can unwrap it later.
        _PATCHES[original] = new_wrapped

        # Wrapped classmethods need to be re-marked as a classmethod so the
        # class is bound as the first argument
        if is_classmethod:
            new_wrapped = classmethod(new_wrapped)

        # A bare method (or a staticmethod) being added to a class need to be
        # re-marked as a staticmethod to prevent them from being bound to the
        # class like an instance method.
        if is_staticmethod:
            new_wrapped = staticmethod(new_wrapped)

        # Overright the original version with our wrapped version
        setattr(base, target, new_wrapped)

        return wrapped
    return wrapper
