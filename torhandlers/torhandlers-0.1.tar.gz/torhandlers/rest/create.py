# -*- coding: utf-8 -*-
__author__ = 'Alex Bo'
__email__ = 'bosha@the-bosha.ru'

import json
from torhandlers.base import log
from torhandlers.exceptions import ImproperlyConfigured
from torhandlers.rest.base import JSONResponseMixin
from torhandlers.rest.form import JSONFormMixin, JSONProcessFormHandler
from torhandlers.utils.serialize import sqlalchemy_orm_to_dict

class JSONProcessCreateHandler(JSONProcessFormHandler):
    """
    TODO: doc
    """

class JSONBaseCreateHandler(JSONFormMixin, JSONProcessCreateHandler):

    def form_valid(self, form):
        if self.model is None:
            raise ImproperlyConfigured(
                "To use %s, need to specify model"  % (self.__class__.__name__)
            )
        try:
            object = self.model(**form.data)
            self.db.add(object)
            self.db.commit()
            self.db.flush()
            self.db.refresh(object)
        except Exception as e:
            self.db.rollback()
            log.error("Error while querying database in %s: %r" % (self.__class__.__name__, e))
            self.render_json_error(errors=['Database query error'])
        finally:
            self.db.flush()

        return self.render_json(context={
            'success': True,
            'errors': None,
            'form': None,
            'object': sqlalchemy_orm_to_dict(object)
        })

class JSONCreateHandler(JSONResponseMixin, JSONBaseCreateHandler):

    def get_json_data(self, context, **kwargs):
        if len(kwargs) > 0:
            context = dict(context, **kwargs)

        if 'form' in context and context['form'] is not None:
            form_html = ''
            for item in context['form']:
                form_html += str(item)
            context['form'] = form_html

        return json.dumps(context, default=str)

