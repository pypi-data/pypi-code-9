import functools
from flask import request, abort, current_app
from .utils import unknown_value


def _value_from_multidict(v):
    if len(v) == 0:
        return None
    elif len(v) == 1:
        return v[0]
    return v


class MissingRequestParam(Exception):
    pass


def get_request_param_value(name, location=None):
    if (not location or location == 'view_args') and name in request.view_args:
        return request.view_args[name]
    if not request.is_json:
        if not location or location == 'values':
            if name in request.values:
                return _value_from_multidict(request.values.getlist(name))
        elif location == 'args' and name in request.args:
            return _value_from_multidict(request.args.getlist(name))
        elif location == 'form' and name in request.form:
            return _value_from_multidict(request.form.getlist(name))
    if (not location or location == 'json') and request.is_json:
        data = request.get_json()
        if isinstance(data, dict) and name in data:
            return data[name]
    if (not location or location == 'files') and name in request.files:
        return _value_from_multidict(request.files.getlist(name))
    raise MissingRequestParam("Request parameter '%s' is missing" % name)


class RequestParam(object):
    def __init__(self, name, type=None, nullable=False, required=False, loader=None, validator=None,
                 dest=None, location=None, help=None, default=unknown_value, **loader_kwargs):
        self.name = name
        self.type = type
        self.nullable = nullable
        self.required = required
        self.loader = loader
        self.loader_kwargs = loader_kwargs
        self.validator = validator
        self.dest = dest
        self.location = location
        self.help = help
        self.default = default

    @property
    def names(self):
        return self.name if isinstance(self.name, tuple) else (self.name,)

    @property
    def dests(self):
        if not self.dest:
            return self.names
        elif not isinstance(self.dest, tuple):
            return (self.dest,)
        return self.dest

    def process(self):
        try:
            values = self.extract()
        except MissingRequestParam:
            if self.required and self.default is unknown_value:
                abort(400)
            elif not self.default is unknown_value:
                if not isinstance(self.name, tuple):
                    values = [self.default]
                else:
                    values = self.default
            else:
                return dict()

        values = self.load(*values)
        if not self.validate(*values):
            abort(400)
        if len(self.dests) != len(values):
            raise Exception('Mismatch between length of dest and number of values')
        return dict(zip(self.dests, values))

    def extract(self):
        values = []
        for name in self.names:
            value = get_request_param_value(name, self.location)
            if value is None and not self.nullable:
                raise MissingRequestParam("Request parameter '%s' is missing" % name)
            if self.type and value is not None:
                try:
                    if self.type is bool:
                        if isinstance(value, (str, unicode)):
                            value = value.lower() in ('true', '0')
                        else:
                            value = bool(value)
                    else:
                        value = self.type(value)
                except Exception as e:
                    current_app.logger.error(e)
                    abort(400)
            values.append(value)
        return values

    def load(self, *values):
        if self.loader:
            rv = self.loader(*values, **self.loader_kwargs)
            if not isinstance(rv, tuple):
                return (rv,)
            return rv
        return values

    def validate(self, *values):
        return not self.validator or self.validator(*values)


def request_param(name, cls=RequestParam, **kwargs):
    def decorator(func):
        if not hasattr(func, '_request_params'):
            func._request_params = []
        func._request_params.append(cls(name, **kwargs))
        return func
    return decorator


def partial_request_param(name=None, **kwargs):
    def decorator(name_=None, **kw):
        return request_param(name_ or name, **dict(kwargs, **kw))
    return decorator


def request_params(params):
    def decorator(func):
        for name, kwargs in params.iteritems():
            request_param(name, **kwargs)(func)
        return func
    return decorator


def request_param_loader(name, **kwargs):
    def decorator(loader_func):
        return request_param(name, loader=loader_func, **kwargs)
    return decorator


def partial_request_param_loader(name=None, **kwargs):
    def decorator(loader_func):
        def partial_gen(name_=None, **kw):
            return request_param(name_ or name, loader=loader_func, **dict(kwargs, **kw))
        return partial_gen
    return decorator


def process_request_params(params):
    values = {}
    for param in params:
        values.update(param.process())
    return values


def inject_request_params(func):
    @functools.wraps(func)
    def wrapper(**kwargs):
        if hasattr(func, '_request_params'):
            kwargs = process_request_params(func._request_params)
        return func(**kwargs)
    return wrapper