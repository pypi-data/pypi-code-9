import re
from django.http import HttpResponseNotAllowed
from django.template.response import TemplateResponse
from functools import wraps


uncamel_patterns = (
    re.compile('(.)([A-Z][a-z]+)'),
    re.compile('([a-z0-9])([A-Z])'),
)


def uncamel(s):
    """
    Make camelcase lowercase and use underscores.
    """
    for pat in uncamel_patterns:
        s = pat.sub(r'\1_\2', s)
    return s.lower()


class Context(object):
    pass


def view(cls):
    """
    View decorator must wrap view class
    """
    @wraps(cls)
    def wrapper(request, **kwargs):
        if hasattr(cls, 'as_view'):
            return cls.as_view()(request, **kwargs)
        obj = cls(request, **kwargs)
        handler = getattr(obj, request.method.lower(), None)
        if handler is None:
            return HttpResponseNotAllowed('%s not allowed' % request.method)
        return obj.setup(obj.c) or handler(obj.c) or obj.render(obj.c)
    return wrapper


class View(object):
    def __init__(self, request, **kwargs):
        self.c = Context()
        self.r = request
        self.u = request.user
        self.c.user = self.u
        for k, v in kwargs.items():
            setattr(self, k, v)

    def setup(self, c):
        pass

    def get_template(self, c):
        if getattr(self, 'template', None):
            return self.template
        app = self.__module__.split('.')[0]
        return '%s/%s.html' % (app, uncamel(self.__class__.__name__))

    def render(self, c):
        return TemplateResponse(self.r, self.get_template(c), c.__dict__)
