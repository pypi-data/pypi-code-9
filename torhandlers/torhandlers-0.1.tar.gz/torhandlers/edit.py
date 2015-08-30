# -*- coding: utf-8 -*-
__author__ = 'Alex Bo'
__email__ = 'bosha@the-bosha.ru'

from torhandlers.base import TemplateResponseMixin, GenericHandler, log, HTTPError
from torhandlers.form import FormMixin, SuccessUrlMixin
from torhandlers.detail import SingleObjectMixin
from torhandlers.utils.serialize import sqlalchemy_orm_to_dict
from torhandlers.exceptions import DatabaseObjectNotFound

class EditObjectMixin(SingleObjectMixin):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.form_initial = sqlalchemy_orm_to_dict(context[self.get_context_object_name()])
        form_class = self.get_form_class()
        context['form'] = self.get_form(form_class)
        return context

    def form_valid(self, form):
        try:
            object = self.get_object()
            for key, val in form.data.items():
                if hasattr(object, key):
                    setattr(object, key, val)
            self.db.commit()
            self.db.flush()
            return super().form_valid(form=form)
        except Exception as e:
            self.db.rollback()
            log.debug(str(e))
            # TODO: maybe create ErrorObj and return it with response with http 500 code?
            raise HTTPError(500)


class ProcessEditHandler(GenericHandler):
    """
    TODO: doc
    """

    def get(self, *args, **kwargs):
        try:
            super().get(*args, **kwargs)
            return self.render(**self.get_context_data())
        except DatabaseObjectNotFound as e:
            log.debug(str(e))
            raise HTTPError(404)

    def post(self, *args, **kwargs):
        super().post(*args, **kwargs)

        try:
            context = self.get_context_data()
        except DatabaseObjectNotFound as e:
            log.debug(str(e))
            raise HTTPError(404)

        if 'form' in context:
            if context['form'].validate():
                return self.form_valid(context['form'])
            else:
                return self.form_invalid(context['form'])
        else:
            raise HTTPError(403)

class BaseEditHandler(EditObjectMixin, FormMixin, SuccessUrlMixin, ProcessEditHandler):
    """
    # TODO: doc
    """

class EditHandler(TemplateResponseMixin, BaseEditHandler):
    """
    TODO: doc
    """
