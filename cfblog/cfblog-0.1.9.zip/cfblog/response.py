__author__ = 'vinay'
from django.core.exceptions import ValidationError
from django.http.response import Http404, HttpResponse
from django.template import TemplateSyntaxError

from .models import Content
from .utils import can_edit_content, parse_cms_template
from .validators import validate_and_get_template


def render(template_name,
           template_context=None, content_type=None, status=None,
           using=None, request=None, cms_context=None):
    """
    Validates the given template and parses it's content
    returning HttpResponse or raising Http404 for syntax and template errors
    that are included in the cms_context

    This function is a hybrid of django's render and render_to_response by removing the deprecated arguments
    This also takes an optional parameter `cms_context` which is used to render the template.
    """
    template = validate_and_get_template(template_name, using=using)
    content = template.render(context=template_context, request=request)

    if request is not None:
        try:
            cms_page = Content.objects.get(url=request.path_info)
        except Content.DoesNotExist:
            pass
        else:
            if can_edit_content(request.user):
                cms_context = cms_page.auth_data
            elif cms_page.is_live:
                return HttpResponse(cms_page.html, content_type, status)

    if cms_context is not None:
        if isinstance(cms_context, dict):
            try:
                content = parse_cms_template(content, cms_context,
                                             publish=False)
            except (ValidationError, TemplateSyntaxError) as e:
                raise Http404(e)
        else:
            raise ValueError('cms_context should be an instance of dict')

    return HttpResponse(content, content_type, status)
