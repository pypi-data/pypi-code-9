# -*- coding: utf-8 -*-
__author__ = 'Alex Bo'
__email__ = 'bosha@the-bosha.ru'

from torhandlers.base import TemplateResponseMixin, HTTPError, log
from torhandlers.exceptions import ImproperlyConfigured
from torhandlers.form import BaseFormHandler

class BaseCreateHandler(BaseFormHandler):
    """
    TODO: doc
    """
    model = None

    def form_valid(self, form):
        if self.model is None:
            raise ImproperlyConfigured(
                "To use %s, need to specify model"  % (self.__class__.__name__)
            )
        try:
            self.db.add(self.model(**form.data))
            self.db.commit()
            self.db.flush()
            return super().form_valid(form=form)
        except Exception as e:
            self.db.rollback()
            log.error("Error while querying database in %s: %r" % (self.__class__.__name__, e))
            raise HTTPError(500)


class CreateHandler(TemplateResponseMixin, BaseCreateHandler):
    """
    #TODO: doc
    """
