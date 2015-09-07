# -*- coding: utf-8 -*-
__author__ = 'Alex Bo'
__email__ = 'bosha@the-bosha.ru'

from torhandlers.base import ContextMixin, GenericHandler, TemplateResponseMixin
from torhandlers.exceptions import ImproperlyConfigured

class SuccessUrlMixin:

    success_url = None
    success_url_name = None

    def get_success_url(self):
        if not self.success_url and not self.success_url_name:
            raise ImproperlyConfigured(
                "success_url or success_url_name should be set to use '%s'" % (self.__class__.__name__)
            )

        if self.success_url_name:
            success_url_name = self.reverse_url(self.success_url_name)
            if success_url_name:
                return success_url_name
            else:
                raise ImproperlyConfigured(
                    "\'%s\' not found in named urls" % (self.success_url_name)
                )

        return self.success_url

class FormMixin(ContextMixin):

    form_initial = None
    form_class = None
    form_excluded_fields = None

    def get_form_initial(self):
        if self.form_initial:
            return self.form_initial
        else:
            return {}

    def get_form_class(self):
        if self.form_class is None:
            raise ImproperlyConfigured(
                "'form_class' should be set and point to Form class in %s" % (self.__class__.__name__)
            )
        return self.form_class

    def get_form(self, form):
        return form(**self.get_form_kwargs())

    def get_excluded_fields(self):
        fields = ['_xsrf', 'id', 'pk']
        if self.form_excluded_fields:
            return fields + self.form_excluded_fields
        else:
            return fields

    def get_form_kwargs(self):
        kwargs = {}
        kwargs.update(self.get_form_initial())
        excluded_fields = self.get_excluded_fields()
        arguments = {}
        for key, val in self.request.arguments.items():
            if key not in excluded_fields:
                arguments[key] = val[0].decode('utf8')
        kwargs.update(arguments)
        return kwargs

    def form_valid(self, form):
        return self.redirect(self.get_success_url())

    def form_invalid(self, form):
        context = self.get_context_data()
        context['form'] = form
        return self.render(**context)

class ProcessFormHandler(GenericHandler):

    def get(self, *args, **kwargs):
        super().get(*args, **kwargs)
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        return self.render(**self.get_context_data(form=form))

    def post(self, *args, **kwargs):
        super().post(*args, **kwargs)
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.validate():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def put(self, *args, **kwargs):
        return self.post(*args, **kwargs)

class BaseFormHandler(FormMixin, SuccessUrlMixin, ProcessFormHandler):
    """
    # TODO:
    """

class FormHandler(TemplateResponseMixin, BaseFormHandler):
    """
    # TODO:
    """
