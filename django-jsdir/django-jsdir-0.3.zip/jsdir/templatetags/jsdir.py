from django import template
from django.utils.safestring import mark_safe

from ..core import JSDir

register = template.Library()


@register.simple_tag
def jsdir(path, **kwargs):
    return mark_safe(JSDir(path, **kwargs).get_tags())
