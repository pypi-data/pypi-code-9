import functools
from copy import copy
from inspect import getargspec, ismethod

from jsonschema.validators import validator_for


class CallError(Exception):
    pass


def _get_validator_cls(validate_args, schema):
    cls = validate_args.get('cls')
    if cls is None:
        cls = validator_for(schema)
    return cls


def _prepare_args(args, arg_names, defaults):
    result = copy(defaults)
    result.update(dict(zip(arg_names, args)))
    return result


def _prepare_kwargs(kwargs, args_to_skip, defaults):
    result = copy(defaults)
    result.update(kwargs)
    for arg_name in args_to_skip:
        result.pop(arg_name, None)
    return result


def validated(schema, args_to_skip=None, validate_args=None):
    if not validate_args:
        validate_args = {}

    args_to_skip = set(args_to_skip) if args_to_skip else set()

    def decorator(f):
        """
        Decorate some method or function in order to validate
        call args or kwargs against specified json-schema.
        :param f: function or method to decorate
        :param schema: json-schema
        :param args_to_skip: list of arguments, which must be skipped
                when validating (for example `request`)
        :param validate_args: arguments to be passed in `jsonschema.validate`.
        :return: decorated function
        """
        validator_cls = _get_validator_cls(validate_args, schema)
        validator_cls.check_schema(schema)

        arg_spec = getargspec(f)
        arg_names = arg_spec.args
        if ismethod(f):
            arg_names = arg_names[1:]  # remove `self` or `cls`

        if args_to_skip:
            arg_names = [a for a in arg_names if a not in args_to_skip]

        defaults = {}
        if arg_spec.defaults:
            def_names = copy(arg_names)
            def_names.reverse()
            def_values = list(arg_spec.defaults)
            def_values.reverse()
            defaults = dict(zip(def_names, def_values))

        def wrapper(*args, **kwargs):
            if args and kwargs:
                raise CallError(
                    "jsonrpc doesn't support calls with both args and kwargs")

            if args:
                params = _prepare_args(args, arg_names, defaults)
            else:
                params = _prepare_kwargs(kwargs, args_to_skip, defaults)

            validator = validator_cls(
                schema, *validate_args.get('args', []),
                **validate_args.get('kwargs', {}))
            validator.validate(params, schema)
            return f(*args) if args else f(**kwargs)

        functools.update_wrapper(wrapper, wrapped=f)
        wrapper.schema = schema
        return wrapper
    return decorator
