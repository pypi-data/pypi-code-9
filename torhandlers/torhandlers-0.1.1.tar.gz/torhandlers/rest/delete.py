# -*- coding: utf-8 -*-
__author__ = 'Alex Bo'
__email__ = 'bosha@the-bosha.ru'

import json
from torhandlers.base import log
from torhandlers.delete import DeletionMixin
from torhandlers.rest.base import JSONGenericHandler, JSONResponseMixin
from torhandlers.detail import SingleObjectMixin
from torhandlers.utils.serialize import sqlalchemy_orm_to_dict
from torhandlers.exceptions import DatabaseObjectNotFound

class JSONProcessDeleteHandler(JSONGenericHandler):

    def get(self, *args, **kwargs):
        super().get(*args, **kwargs)
        try:
            context = self.get_context_data(**kwargs)
            obj_name = self.get_context_object_name()
            context[obj_name] = sqlalchemy_orm_to_dict(context[obj_name])
            return self.render_json(context)
        except (RuntimeError, DatabaseObjectNotFound) as e:
            log.debug(str(e))
            return self.render_json_error(errors=[str(e)])
        except Exception as e:
            log.error(str(e))
            return self.render_json_error(
                errors=['Something really bad happens..']
            )

    def post(self, *args, **kwargs):
        super().post(*args, **kwargs)
        try:
            self.delete_obj()
            self.db.remove()
            return self.render_json(context={'success': True, 'errors': None})
        except (RuntimeError, DatabaseObjectNotFound) as e:
            log.debug(str(e))
            return self.render_json_error(errors=[str(e)])
        except Exception as e:
            log.error(str(e))
            return self.render_json_error(
                errors=['Something really bad happens..']
            )

class JSONBaseDeleteHandler(SingleObjectMixin, DeletionMixin, JSONProcessDeleteHandler):
    """
    # TODO: document
    """

class JSONDeleteHandler(JSONResponseMixin, JSONBaseDeleteHandler):

    def get_json_data(self, context, **kwargs):
        return json.dumps(context, default=str)
