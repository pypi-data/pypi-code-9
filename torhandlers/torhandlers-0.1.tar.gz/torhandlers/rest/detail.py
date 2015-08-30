# -*- coding: utf-8 -*-
__author__ = 'Alex Bo'
__email__ = 'bosha@the-bosha.ru'

import json
from torhandlers.base import log
from torhandlers.rest.base import JSONResponseMixin, JSONGenericHandler
from torhandlers.detail import SingleObjectMixin
from torhandlers.utils.serialize import sqlalchemy_orm_to_dict
from torhandlers.exceptions import DatabaseObjectNotFound

class JSONProcessDetailHandler(JSONGenericHandler):

    def get(self, *args, **kwargs):
        super().get(*args, **kwargs)
        try:
            return self.render_json(context=self.get_context_data())
        except DatabaseObjectNotFound as e:
            log.debug(str(e))
            return self.render_json_error(errors=[str(e)])


class JSONBaseDetailHandler(SingleObjectMixin, JSONProcessDetailHandler):
    """
    TODO: doc
    """

class JSONDetailHandler(JSONResponseMixin, JSONBaseDetailHandler):

    def get_json_data(self, context, **kwargs):

        if len(kwargs) > 0:
            context = dict(context, **kwargs)

        obj_name = self.get_context_object_name()

        try:
            context[obj_name] = sqlalchemy_orm_to_dict(context[obj_name])
        except RuntimeError:
            log.error("%r is not JSON serializable" % (context[obj_name]))
            context[obj_name] = dict

        return json.dumps(context, default=str)
