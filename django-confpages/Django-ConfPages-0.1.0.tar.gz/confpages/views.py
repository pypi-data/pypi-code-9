from __future__ import absolute_import

import requests
from django.views.generic import View
from django.shortcuts import render
from django.http import (
    HttpResponse,
    HttpResponseForbidden,
    HttpResponseNotAllowed,
    HttpResponseServerError
)
from django.template import Template, Context
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
try:
    from django.utils.module_loading import import_string
except ImportError:
    # `import_string` is introduced in Django 1.7,
    # use the copy utility for older versions.
    from .utils import import_string

from .conf import settings
from .token import check_token


class ConfPages(View):
    """The core view class for the configurable pages."""

    # The loader of pages
    page_loader = import_string(settings.PAGE_LOADER)()

    # The client of the backend API
    client = requests.api

    def render_content(self, content, is_static, api_url):
        """Render the content if it's non-static or if it contains
        any one-time token tag.
        """
        token_tag_string = '{% one_time_token %}'
        if is_static and token_tag_string not in content:
            return content

        # Get the context from the backend API if the page is non-static
        context = {}
        if not is_static and api_url:
            response = self.client.get(api_url)
            context = response.json()

        # Add the `load` tag if the page contains any one-time token tag
        if token_tag_string in content:
            content = '{% load confpages_tags %}\n' + content

        template = Template(content)
        return template.render(Context(context))

    def get(self, request, name):
        """Show the page whose name is `name`."""
        page = self.page_loader.get_page(name)
        rendered_content = self.render_content(page.content, page.is_static,
                                               page.api_url)

        if not page.base_template:
            return HttpResponse(rendered_content)
        else:
            context = {
                'name': page.name,
                'title': page.title,
                'content': rendered_content
            }
            return render(request, page.base_template, context)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        """Override to make dispatch() CSRF exempt."""
        return super(ConfPages, self).dispatch(request, *args, **kwargs)

    def post(self, request, name):
        """Handle the form submission by delegating the request to
        the backend API.

        Note:
            The data the API consumes or produces is encoded in JSON.
        """
        data = request.POST.dict().copy()
        token = data.pop('_onetimetoken', None)
        method = data.pop('_method', None) or request.method

        # If the one-time token is valid, reject the request
        is_valid, reason = check_token(token)
        if not is_valid:
            return HttpResponseForbidden(reason, content_type='text/html')

        page = self.page_loader.get_page(name, only_api_url=True)
        if not page.api_url:
            return HttpResponseNotAllowed(['GET'])

        # Delegate the request to the API
        response = self.client.request(method, page.api_url, json=data)
        if response.status_code == 404:
            return HttpResponseServerError('The backend API can not be found')
        else:
            return HttpResponse(
                response.content,
                response.headers['Content-Type'],
                response.status_code
            )
