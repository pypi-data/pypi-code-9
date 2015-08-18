# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
from django.conf import settings
from django.core.urlresolvers import RegexURLResolver
import sys


def url_pattern(url_pattern_regex, url_parent=''):
    callback = None
    url = url_parent
    if url and url[0] == '^':
        url = url[1:]

    url_parent = url_pattern_regex._regex

    try:
        callback = url_pattern_regex.callback.__dict__
        if 'cls' in callback and all(list(filter(lambda x: x.__name__ == 'APIView', callback['cls'].mro()))):
            callback = callback['cls']
        else:
            callback = None
    except AttributeError:
        pass

    if url_parent and url_parent[0] == '^':
        url_parent = url_parent[1:]

    url = '/%s%s' % (url, url_parent)
    url = url.replace('\.(?P<format>\w+)$', '.json').replace('?P', '')
    url = re.sub(r'[\?\$\^]+', '', url, re.IGNORECASE)
    url = url.strip('/').split('/')

    def ulr_format(item):
        arg = ':arg'
        item = re.sub(r'(\\\w?)+', '', item, re.IGNORECASE)
        p = re.compile(ur'\<(?P<name>\w+)\>', re.IGNORECASE)
        match = re.findall(p, item)

        if len(match) == 1:
            arg = match[0]

        item = re.sub(r'([^a-zА-Я0-9_-])+', '', item, re.IGNORECASE)

        if item == '':
            item = arg
        elif arg == item:
            item = ':%s' % arg
        return item
    url = list(map(ulr_format, url))

    if not all(url) or len(url) == 1 and url[0] == ':arg':
        url = ['']
    else:
        url = [''] + url

    url.append('')
    url = '/'.join(url)

    return url, callback


def search_ulrs():
    __import__(settings.ROOT_URLCONF)
    urls = sys.modules[settings.ROOT_URLCONF]
    urls_pars = []
    for url in urls.urlpatterns:
        if isinstance(url, RegexURLResolver):
            urls_pars += list(map(lambda x: url_pattern(x, url._regex), url.url_patterns))
        else:
            urls_pars += [url_pattern(url, '')]
    return list(filter(lambda x: x[1] is not None, urls_pars))
