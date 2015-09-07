# -*- coding: utf-8 -*-
__author__ = 'Alex Bo'
__email__ = 'bosha@the-bosha.ru'

import json
from torhandlers.base import log
from torhandlers.rest.base import JSONResponseMixin
from torhandlers.rest.form import JSONProcessFormHandler, JSONFormMixin
from torhandlers.detail import SingleObjectMixin
from torhandlers.utils.serialize import sqlalchemy_orm_to_dict
from torhandlers.exceptions import DatabaseObjectNotFound

class JSONProccessEditHandler(JSONFormMixin, JSONProcessFormHandler):
    """
    TODO: document
    """


class JSONBaseEditHandler(SingleObjectMixin, JSONProccessEditHandler):

    def form_valid(self, form):
        try:
            object = self.get_object()
            for key, val in form.data.items():
                if hasattr(object, key):
                    setattr(object, key, val)
            self.db.commit()
            self.db.flush()
            return self.render_json(context={'success': True, 'errors': None, 'form': None, 'object': object })
        except DatabaseObjectNotFound as e:
            log.debug(str(e))
            self.render_json_error(errors=[str(e)])
        except Exception as e:
            self.db.rollback()
            log.error("Error while querying database in %s: %r" % (self.__class__.__name__, e))
            return self.render_json_error(errors=['Database query error'])


class JSONEditHandler(JSONResponseMixin, JSONBaseEditHandler):

    def get_json_data(self, context, **kwargs):
        if len(kwargs) > 0:
            context = dict(context, **kwargs)

        if 'form' in context and context['form'] is not None:
            form_html = ''
            for item in context['form']:
                form_html += str(item)
            context['form'] = form_html

        obj_name = self.get_context_object_name()

        if obj_name in context:
            try:
                context[obj_name] = sqlalchemy_orm_to_dict(context[obj_name])
            except RuntimeError:
                log.error("%r is not JSON serializable" % (context[obj_name]))
                context[obj_name] = dict

        return json.dumps(context, default=str)
