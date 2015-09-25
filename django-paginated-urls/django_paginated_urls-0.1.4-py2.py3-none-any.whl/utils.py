# -*- coding: utf-8 -*-

"""

"""


def add_page_to_url(request, url):
    latest_paginated_url = request.session.get('latest_paginated_url')
    if latest_paginated_url and latest_paginated_url['path'] == url:
        url = '{}?page={}'.format(url, latest_paginated_url['page'])
    return url