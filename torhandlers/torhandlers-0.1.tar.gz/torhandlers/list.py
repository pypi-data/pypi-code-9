# -*- coding: utf-8 -*-
__author__ = 'Alex Bo'
__email__ = 'bosha@the-bosha.ru'

import math
from torhandlers.exceptions import ImproperlyConfigured
from torhandlers.base import ContextMixin, GenericHandler, TemplateResponseMixin
from torhandlers.pagination import Page

from sqlalchemy import func

class MultipleObjectsMixin(ContextMixin):

    model = None
    queryset = None
    context_object_name = None
    paginate_by = None
    paginator_page_kwarg = 'page'
    _cached_pages_count = None

    def get_queryset(self):
        if self.queryset is not None:
            queryset = self.queryset
        elif self.model is not None:
            try:
                queryset = self.db.query(self.model).all()
                self.db.commit()
            except:
                self.db.rollback()
                raise LookupError(
                    "There was error querying the database"
                )
            finally:
                self.db.flush()
        else:
            raise ImproperlyConfigured(
                "%s required to configure \'model\' or \'queryset\' property" % (self.__class__.__name__)
            )
        return queryset

    def get_paginated_queryset(self, paginate_by, current_page, pages_count):

        if self.model is None:
            raise ImproperlyConfigured(
                "%s required to configure \'model\' or \'queryset\' property" % (self.__class__.__name__)
            )

        if current_page > pages_count:
            offset = 0
        else:
            offset = current_page * paginate_by - paginate_by

        return self.db.query(self.model).limit(paginate_by).offset(offset).all()

    def get_context_object_name(self):
        if self.context_object_name:
            return self.context_object_name
        else:
            return 'objects_list'

    def get_context_data(self, **kwargs):
        paginate_by = self.get_paginate_by()
        context = super().get_context_data(**kwargs)
        if paginate_by:
            pages_count = self.get_pages_count()
            current_page = self.get_current_page_number()
            queryset = self.get_paginated_queryset(paginate_by, current_page, pages_count)
            context['is_paginated'] = False if pages_count <= 1 else True
            context['page_obj'] = Page(
                pages_number=pages_count,
                current_page=current_page,
                items_number=paginate_by
            )
            self._cached_pages_count = None
        else:
            queryset = self.get_queryset()
            context['is_paginated'] = False
            context['page_obj'] = None
        context[self.get_context_object_name()] = queryset
        return context

    def get_paginate_by(self):
        return self.paginate_by

    def get_page_kwarg(self):
        return self.paginator_page_kwarg

    def get_current_page_number(self):
        page_kwarg = self.get_page_kwarg()
        if page_kwarg in self.kwargs:
            page = self.kwargs.get('page')[0]
            page = page.decode('utf8')
            if page == 'last':
                return self.get_pages_count()

            page = int(page)
            if page == 0:
                return 1
            else:
                return page

        return 1

    def get_pages_count(self):
        if self._cached_pages_count is None:
            obj_count = self.db.query(func.count(self.model.id)).scalar()
            count = int(math.ceil(obj_count / self.paginate_by))
            self._cached_pages_count = count if count != 0 else 1
        return self._cached_pages_count

class ProcessListHandler(GenericHandler):

    def get(self, *args, **kwargs):
        super().get(*args, **kwargs)
        context = self.get_context_data()
        return self.render(**context)

    def post(self, *args, **kwargs):
        return self.get(*args, **kwargs)

class BaseListHandler(MultipleObjectsMixin, ProcessListHandler):
    """
    # TODO: doc
    """

class ListHandler(TemplateResponseMixin, BaseListHandler):
    """
    # TODO: doc
    """
