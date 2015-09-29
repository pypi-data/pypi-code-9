# -*- coding: utf-8 -*-

"""

"""


class PaginatedURLMiddleware():
    def process_view(self, request, view_func, view_args, view_kwargs):
        """
        :param request:
        :param view_func:
        :param view_args:
        :param view_kwargs:
        :return: HttpResponse (returned from calling view_func)
        """
        page = request.GET.get('page')
        if page:
            request.session['latest_paginated_url'] = dict(
                path=request.path,
                page=page
            )
        return None  # continue processing the view