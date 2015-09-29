# -*- coding: utf-8 -*-

"""

"""

from django.core.urlresolvers import reverse

from .utils import add_page_to_url


def paginated_reverse(request, viewname, *args, **kwargs):
    force_page = kwargs.pop('force_page', None)
    url = reverse(viewname, *args, **kwargs)
    return add_page_to_url(request, url, force_page=force_page)
