# -*- coding: utf-8 -*-
__author__ = 'Alex Bo'
__email__ = 'bosha@the-bosha.ru'

from sqlalchemy.orm.exc import NoResultFound
from torhandlers.base import GenericHandler, ContextMixin, TemplateResponseMixin, log, HTTPError
from torhandlers.exceptions import ImproperlyConfigured, DatabaseObjectNotFound

class SingleObjectMixin(ContextMixin):

    model = None
    queryset = None
    slug_field = None
    context_object_name = None
    slug_url_kwarg = None
    pk_url_kwarg = None
    object = None

    def get_object(self, queryset=None):

        if self.object is not None:
            return self.object

        if queryset is None:
            queryset = self.get_queryset()

        pk = self.kwargs.get(self.pk_url_kwarg, None)
        slug = self.kwargs.get(self.slug_url_kwarg, None)
        slug_field = self.kwargs.get(self.slug_field, None)

        if pk is not None:
            queryset = queryset.filter(self.model.id == pk)
        elif slug is not None and slug_field is not None:
            queryset = queryset.filter(slug_field == slug)
        else:
            raise ImproperlyConfigured(
                "Detail View %s must be called with either"
                "an object pk or slug" % (self.__class__.__name__)
            )

        try:
            obj = queryset.one()
            self.object = obj
        except NoResultFound:
            raise DatabaseObjectNotFound("No {} matching query found".format(self.model.__name__))

        return self.object

    def get_queryset(self):
        if self.queryset is None:
            if self.model:
                self.queryset = self.db.query(self.model)
            else:
                raise ImproperlyConfigured(
                    "%s required to configure \'model\' or \'queryset\' property" % (self.__class__.__name__)
                )
        return self.queryset

    def get_slug_field(self):
        return self.slug_field

    def get_context_object_name(self):
        if self.context_object_name:
            return self.context_object_name
        else:
            return 'object'

    def get_context_data(self, **kwargs):
        context = super(SingleObjectMixin, self).get_context_data(**kwargs)
        context[self.get_context_object_name()] = self.get_object()
        return context

class ProcessDetailHandler(GenericHandler):

    def get(self, *args, **kwargs):
        super().get(*args, **kwargs)
        try:
            return self.render(**self.get_context_data())
        except DatabaseObjectNotFound as e:
            log.debug(str(e))
            raise HTTPError(404)

class BaseDetailHandler(SingleObjectMixin, ProcessDetailHandler):
    """
    TODO: doc
    """

class DetailHandler(TemplateResponseMixin, BaseDetailHandler):
    """
    TODO: doc
    """
