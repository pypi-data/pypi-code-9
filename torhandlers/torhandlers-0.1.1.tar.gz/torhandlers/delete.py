# -*- coding: utf-8 -*-
__author__ = 'Alex Bo'
__email__ = 'bosha@the-bosha.ru'

from torhandlers.base import TemplateResponseMixin, log, HTTPError
from torhandlers.form import SuccessUrlMixin
from torhandlers.detail import BaseDetailHandler
from torhandlers.exceptions import DatabaseObjectNotFound

class DeletionMixin:
    def delete_obj(self, *args, **kwargs):
        self.db.delete(self.get_object())
        self.db.commit()

class ProcessDeleteHandler(BaseDetailHandler):

    def post(self, *args, **kwargs):
        super().post(*args, **kwargs)
        try:
            self.delete_obj()
            self.db.remove()
        except (DatabaseObjectNotFound) as e:
            log.debug(str(e))
            raise HTTPError(404)
        except Exception as e:
            log.error(str(e))
            raise HTTPError(500)

        return self.redirect(self.get_success_url())


class BaseDeleteHandler(DeletionMixin, SuccessUrlMixin, ProcessDeleteHandler):
    """
    TODO: doc
    """


class DeleteHandler(TemplateResponseMixin, BaseDeleteHandler):
    """
    TODO: doc
    """
