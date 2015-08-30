# -*- coding: utf-8 -*-
__author__ = 'Alex Bo'
__email__ = 'bosha@the-bosha.ru'

import json
from torhandlers.base import log
from torhandlers.rest.base import JSONGenericHandler, JSONResponseMixin
from torhandlers.list import MultipleObjectsMixin
from torhandlers.utils.serialize import sqlalchemy_orm_to_dict

class JSONProcessListHandler(JSONGenericHandler):
    def post(self, *args, **kwargs):
        super().post(*args, **kwargs)
        return self.render_json(context={'success': False, 'errors': {'error': "Not available"}})

    def get(self, *args, **kwargs):
        super().get(*args, **kwargs)
        context = self.get_context_data()
        context['success'] = True
        context['errors'] = []
        return self.render_json(context)

class JSONBaseListHandler(MultipleObjectsMixin, JSONProcessListHandler):
    """
    TODO: doc
    """

class JSONListHandler(JSONResponseMixin, JSONBaseListHandler):
    """
    TODO: doc
    """
    def get_json_data(self, context, **kwargs):

        if len(kwargs) > 0:
            context = dict(context, **kwargs)

        obj_name = self.get_context_object_name()
        new_data = []

        if context['is_paginated']:
            context['page_obj'] = context['page_obj'].as_dict

        if type(context[obj_name]) == list:
            for item in context[obj_name]:
                try:
                    new_data.append(sqlalchemy_orm_to_dict(item))
                except RuntimeError:
                    log.error("%r is not JSON serializable" % (item))

        context[obj_name] = new_data
        return json.dumps(context, default=str)
