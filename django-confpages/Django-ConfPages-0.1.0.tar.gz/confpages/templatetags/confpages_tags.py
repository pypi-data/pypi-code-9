from __future__ import absolute_import

from django import template
from django.utils.safestring import mark_safe

from ..token import make_token

register = template.Library()


@register.simple_tag
def one_time_token():
    token = make_token()
    html = mark_safe(u'<input type="hidden" name="_onetimetoken" '
                     'value="{}" />'.format(token))
    return html
