# -*- coding: utf-8 -*-

"""

"""

from django.core.urlresolvers import reverse

from .utils import add_page_to_url


def paginated_reverse(request, url_name, **kwargs):
    url = reverse(viewname=url_name, **kwargs)
    return add_page_to_url(request, url)
