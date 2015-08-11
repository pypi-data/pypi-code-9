from django.conf import settings
from django.test.client import RequestFactory
from django.template import RequestContext
from cms.plugin_rendering import render_placeholder
from django.contrib.auth.models import AnonymousUser


def get_request(language=None):
    request_factory = RequestFactory()
    request = request_factory.get('/')
    request.session = {}
    request.LANGUAGE_CODE = language or settings.LANGUAGE_CODE

    # Needed for plugin rendering.
    request.current_page = None
    request.user = AnonymousUser()

    return request


def render_placeholderfield(placeholderfield, language=None):
    request = get_request(language)
    content = render_placeholder(placeholderfield, RequestContext(request))

    return content
