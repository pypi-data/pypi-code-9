# -*- coding: utf-8 -*-
__author__ = 'Alex Bo'
__email__ = 'bosha@the-bosha.ru'

import logging
import tornado
import tornado.web
from tornado.web import HTTPError
from torhandlers.exceptions import ImproperlyConfigured
from torhandlers.templating import TornadoTemplater

log = logging.getLogger(__name__)

class GenericHandler(tornado.web.RequestHandler):

    def initialize(self):
        self.kwargs = {}
        for key, val in self.request.arguments.items():
            self.kwargs[key] = val

    def get(self, *args, **kwargs):
        self.args = args
        self.kwargs.update(kwargs)

    def post(self, *args, **kwargs):
        self.args = args
        self.kwargs.update(kwargs)

    def get_error_html(self, status_code, **kwargs):
        self.set_status(status_code=status_code)
        self.write("<html><body><h1>Error</h1></body></html>")

    def request_ajax(self):
        return "X-Requested-With" in self.request.headers and \
               self.request.headers['X-Requested-With'] == "XMLHttpRequest"

    def get_param(self, name, default=None):
        param = self.get_params(name=name, default=default)
        if param:
            return param[0]
        return default

    def get_params(self, name, default=None):
        if name in self._get_args:
            return self._get_args[name]
        else:
            return default

    @property
    def db(self):
        return self.application.db

    @property
    def settings(self):
        return self.application.settings

    @property
    def env(self):
        return self.application.env

    def on_finish(self):
        # This is not a best idea every request/response cycle close db connection,
        # especially if no database connection required (TemplateHandler, for example).
        # FIXME: close database connection only when database used
        self.db.close()
        super().on_finish()

class TemplateResponseMixin:

    template_name = None

    def render(self, **kwargs):
        if not self.template_name:
            raise ImproperlyConfigured("Need to set template_name to use TemplateHandler")

        if not 'templater' in self.settings:
            raise ImproperlyConfigured(
                "templater should be defined in settings"
            )

        templater = self.settings['templater']
        if issubclass(templater, TornadoTemplater):
            return super().render(self.template_name, **kwargs)
        return templater(self).render(**kwargs)

class ContextMixin:

    context = None

    def get_context_data(self, **kwargs):
        if len(kwargs) > 0:
            self.context = {}
            for key, val in kwargs.items():
                self.context[key] = val
        else:
            self.context = {}
        return self.context

class TemplateHandler(TemplateResponseMixin, ContextMixin, GenericHandler):

    def get(self, *args, **kwargs):
        super().get(*args, **kwargs)
        context = self.get_context_data(**kwargs)
        return self.render(**context)

class RedirectHandler(GenericHandler):

    url = None
    pattern = None
    permanent = False

    def get_redirect_url(self):
        url = None
        if self.url:
            url =  self.url
        elif self.pattern:
            try:
                url = self.reverse_url(self.pattern)
            except KeyError as e:
                return None
        return url

    def get(self, *args, **kwargs):
        super().get(*args, **kwargs)
        url = self.get_redirect_url()
        if url is None:
            raise ImproperlyConfigured(
                'To use RedirectHandler need to specify redirect_url or redirect_pattern'
                'in %s' % (self.__class__.__name__)
            )
        self.redirect(url=url, permanent=self.permanent)
