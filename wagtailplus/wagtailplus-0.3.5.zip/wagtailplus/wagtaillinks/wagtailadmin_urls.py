"""
Contains Wagtail admin URL overrides.
"""
from django.conf.urls import url

from .forms import EmailLinkForm
from .forms import ExternalLinkForm
from .models import (
    EmailLink,
    ExternalLink
)
from .views.chooser import LinkChooser


urlpatterns = [
    # Override Wagtail's default embedded link views.
    url(
        r'^links-choose-email/$',
        LinkChooser.as_view(
            model           = EmailLink,
            form_class      = EmailLinkForm,
            url_namespace   = 'wagtaillinks',
            template_dir    = 'wagtaillinks/chooser'
        ),
        name='wagtailadmin_choose_page_email_link'
    ),
    url(
        r'^links-choose-external/$',
        LinkChooser.as_view(
            model           = ExternalLink,
            form_class      = ExternalLinkForm,
            url_namespace   = 'wagtaillinks',
            template_dir    = 'wagtaillinks/chooser'
        ),
        name='wagtailadmin_choose_page_external_link'
    ),
]
