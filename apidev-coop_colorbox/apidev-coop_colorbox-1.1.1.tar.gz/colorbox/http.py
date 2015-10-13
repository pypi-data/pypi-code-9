# -*- coding: utf-8 -*-

from django.http import HttpResponse


class HttpResponseClosePopup(HttpResponse):
    """A HttpResponse with the right content for closing the colorbox"""
    def __init__(self):
        super(HttpResponseClosePopup, self).__init__("close_popup")


class HttpResponseReloadPopup(HttpResponse):
    """A HttpResponse with the right content for loading the view in a new colorbox"""
    def __init__(self, url):
        super(HttpResponseReloadPopup, self).__init__(u'reload: {0}'.format(url))


class HttpResponseRedirectPopup(HttpResponse):
    """A HttpResponse with the right content for closing the popup and go to a different page"""
    def __init__(self, url):
        super(HttpResponseRedirectPopup, self).__init__(
            u'<script>$.colorbox.close(); window.location="{0}";</script>'.format(url)
        )
