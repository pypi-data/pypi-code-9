# -*- coding: utf-8 -*-
"""decorator for managing colorbox"""

import logging

from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseForbidden
from django.core.exceptions import PermissionDenied

logger = logging.getLogger("colorbox")


def popup_redirect(view_func):
    """manage redirection : close the coorbox. Very useful for form-based views"""
    def wrapper(request, *args, **kwargs):
        try:
            response = view_func(request, *args, **kwargs)
        except Http404:
            return HttpResponseNotFound()
        except PermissionDenied:
            return HttpResponseForbidden()    
        except Exception, msg:
            logger.exception(u"exception in popup: {0}".format(msg))
            raise
        if response.status_code == 302:
            script = u'<script>$.colorbox.close(); window.location="{0}";</script>'.format(response['Location'])
            return HttpResponse(script)
        elif response.status_code != 200:
            return HttpResponse(status_code=response.status_code)
        else:
            return response
    return wrapper


def popup_reload(view_func):
    """manage redirection : reopen in a new coorbox."""
    def wrapper(request, *args, **kwargs):
        try:
            response = view_func(request, *args, **kwargs)
        except Http404:
            return HttpResponseNotFound()
        except PermissionDenied:
            return HttpResponseForbidden()
        except Exception, msg:
            logger.exception(u"exception in popup: {0}".format(msg))
            raise
        if response.status_code == 302:
            script = u'reload: {0}'.format(response['Location'])
            return HttpResponse(script)
        elif response.status_code != 200:
            return HttpResponse(status_code=response.status_code)
        else:
            return response
    return wrapper


def popup_close(view_func):
    """close the popup but don't leave the page"""

    def wrapper(request, *args, **kwargs):
        response = view_func(request, *args, **kwargs)
        if not response:
            script = '<script>$.colorbox.close(); window.location=window.location;</script>'
            response = HttpResponse(script)
        return response
    return wrapper
