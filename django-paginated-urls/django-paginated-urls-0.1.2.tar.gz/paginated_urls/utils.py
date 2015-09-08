# -*- coding: utf-8 -*-

"""

"""


def add_page_to_url(request, url_name, url):
    if request.user.is_authenticated():
        latest_paginated_url = request.session.get('latest_paginated_url')
        if latest_paginated_url['url_name'] == url_name:
            url = '{}?page={}'.format(url, latest_paginated_url['page'])
    return url