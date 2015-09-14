# -*- coding: utf-8 -*-

from django.conf import settings

BASE_TEMPLATE = getattr(settings, 'DOCSFROMTESTS_BASE_TEMPLATE', 'gitlab.tpl')
REQUEST_TEMPLATE = getattr(settings, 'DOCSFROMTESTS_REQUEST_TEMPLATE', 'gitlab_request.tpl')
DOCS_PATH = getattr(settings, 'DOCSFROMTESTS_DOCS_PATH', 'docs')
REQUEST_KWARGS = getattr(settings, 'DOCSFROMTESTS_REQUEST_KWARGS', {})
FILE_FORMAT = getattr(settings, 'DOCSFROMTESTS_FILE_FORMAT', 'md')
