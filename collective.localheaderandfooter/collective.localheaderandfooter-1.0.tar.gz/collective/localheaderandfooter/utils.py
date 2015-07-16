# -*- coding: utf8 -*-

import logging

from zope.component import getUtility
from zope.component import queryMultiAdapter

from plone.registry.interfaces import IRegistry

from .behavior import IHeaderAndFooter

logger = logging.getLogger('LocalHeaderAndFooter')


def _get_options(key):
    res = []
    registry = getUtility(IRegistry)
    try:
        settings = registry[key].encode('utf-8')
    except KeyError:
        msg = 'Missing "%s" in registry' % key
        logger.error(msg)
        return res

    for i, entry in enumerate(settings.splitlines()):
        if entry.strip():
            # non emtpy line
            try:
                name, title = entry.split('|')
                res.append({
                    'name': name,
                    'title': title,
                })
            except ValueError:
                msg = 'Error in %s settings. ' % key
                msg += 'Line %s: "%s"' % (i, entry)
                logger.error(msg)
    return res


def get_available_headers():
    key = 'localheaderandfooter.headers'
    return _get_options(key)


def get_available_footers():
    key = 'localheaderandfooter.footers'
    return _get_options(key)


def _get_local_name(context, fname):
    behavior = IHeaderAndFooter(context, None)
    if behavior and getattr(behavior, fname, None):
        return getattr(behavior, fname)
    return None


def get_local_header_name(context):
    return _get_local_name(context, 'custom_header')


def get_local_footer_name(context):
    return _get_local_name(context, 'custom_footer')


def _get_local(context, request, name):
    if not name:
        return None
    # 1st look for acquired templates
    template = getattr(context, name, None)
    if template and True:  # TODO: check for real template object
        return template()
    # 2nd look for views
    view = queryMultiAdapter((context, request),
                             name=name)
    if view:
        return view()
    return None


def get_local_header(context, request):
    name = get_local_header_name(context)
    return _get_local(context, request, name)


def get_local_footer(context, request):
    name = get_local_footer_name(context)
    return _get_local(context, request, name)
