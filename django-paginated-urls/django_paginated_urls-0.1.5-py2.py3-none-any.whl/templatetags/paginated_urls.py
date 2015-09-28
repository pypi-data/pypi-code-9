# -*- coding: utf-8 -*-

"""

"""

from django import template
from django.template.defaulttags import (
    url as django_url_tag,
    URLNode)

from ..utils import add_page_to_url

register = template.Library()


class PaginatedURLNode(URLNode):
    def render(self, context):
        url = super().render(context)
        return add_page_to_url(context['request'], url)


@register.tag
def paginated_url(parser, token):
    dj_node = django_url_tag(parser, token)
    node = PaginatedURLNode(
        view_name=dj_node.view_name,
        args=dj_node.args,
        kwargs=dj_node.kwargs,
        asvar=dj_node.asvar
    )
    return node
