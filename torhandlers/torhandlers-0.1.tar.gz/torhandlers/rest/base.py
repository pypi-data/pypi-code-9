# -*- coding: utf-8 -*-
__author__ = 'Alex Bo'
__email__ = 'bosha@the-bosha.ru'

import json
from torhandlers.base import GenericHandler, ContextMixin, HTTPError

class JSONResponseMixin:

    def render_json(self, context, **kwargs):
        data = self.get_json_data(context=context, **kwargs)
        self.write(data)
        self.set_header('Content-Type', 'application/json')
        self.finish()

    def get_json_data(self, context, **kwargs):
        raise NotImplementedError(
            "get_json_data should be implemented in %s" % (self.__class__.__name__)
        )

    def render_json_error(self, status_code=500, errors=None, **kwargs):
        context = {
            'success': False,
            'errors': errors
        }

        if len(kwargs) > 0:
            context.update(kwargs)

        self.set_status(status_code)
        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(context))
        self.finish()

class JSONGenericHandler(GenericHandler):

    def initialize(self):
        super().initialize()
        if self.request_ajax() is False:
            raise HTTPError(403)

class JSONTemplateHandler(JSONResponseMixin, ContextMixin, JSONGenericHandler):

    def get(self, *args, **kwargs):
        super().get(*args, **kwargs)
        context = self.get_context_data(**kwargs)
        return self.render_json(context=context)
