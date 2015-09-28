# -*- coding: utf-8 -*-

"""

"""

from django.http import Http404, HttpResponseRedirect


class RedirectToLastPageException(Exception):
    pass


class RedirectInvalidPageToLastPageMixin(object):
    def paginate_queryset(self, queryset, page_size):
        try:
            result = super().paginate_queryset(queryset, page_size)
        except Http404 as e:
            raise RedirectToLastPageException(e)
        return result

    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except RedirectToLastPageException as e:
            page_kwarg = self.page_kwarg
            page = self.kwargs.get(page_kwarg) or self.request.GET.get(page_kwarg) or 1
            if page != 'last':
                get_args = self.request.GET.copy()
                get_args['page'] = 'last'
                last_url = '{}?{}'.format(self.request.path, get_args.urlencode())
                return HttpResponseRedirect(last_url)
            else:
                raise e.args[0]
