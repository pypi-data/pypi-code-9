# -*- coding: utf-8 -*-

"""

"""


def add_page_to_url(request, url, force_page=None):
    latest_paginated_url = request.session.get('latest_paginated_url')
    if latest_paginated_url and (force_page or latest_paginated_url.get('path') == url):
        # if we're using force_page, we're not just trying to get whichever page was the last one
        # TODO: build query string in a more robust way
        url = '{}?page={}'.format(url, force_page or latest_paginated_url['page'])
    return url


def override_page_for_url(request, url, page):
    request.session['latest_paginated_url'] = dict(path=url, page=page)
