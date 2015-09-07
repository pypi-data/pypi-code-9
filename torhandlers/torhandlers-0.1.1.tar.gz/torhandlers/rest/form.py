# -*- coding: utf-8 -*-
__author__ = 'Alex Bo'
__email__ = 'bosha@the-bosha.ru'

import json
from torhandlers.base import log
from torhandlers.form import FormMixin
from torhandlers.rest.base import JSONGenericHandler, JSONResponseMixin
from torhandlers.exceptions import DatabaseObjectNotFound

class JSONFormMixin(FormMixin):

    def form_valid(self, form):
        return self.render_json(context={'success': True, 'errors': None})

    def form_invalid(self, form):
        return self.render_json_error(errors=[form.errors])

class JSONProcessFormHandler(JSONGenericHandler):

    def get(self, *args, **kwargs):
        super().get(*args, **kwargs)
        try:
            context = self.get_context_data()
            form_class = self.get_form_class()
            form = self.get_form(form_class)
            context['form'] = form
            return self.render_json(context)
        except DatabaseObjectNotFound as e:
            log.debug(str(e))
            return self.render_json_error(errors=[str(e)])

    def post(self, *args, **kwargs):
        super().post(*args, **kwargs)
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.validate():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

class JSONBaseFormHandler(JSONFormMixin, JSONProcessFormHandler):
    """
    # TODO: doc
    """

class JSONFormHandler(JSONResponseMixin, JSONBaseFormHandler):
    """
    # TODO: doc
    """
    def get_json_data(self, context, **kwargs):
        if len(kwargs) > 0:
            context = dict(context, **kwargs)

        if 'form' in context:
            form_html = ''
            for item in context['form']:
                form_html += str(item)
            context['form'] = form_html

        return json.dumps(context, default=str)
