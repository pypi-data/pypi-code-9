from django import template
from richcontentblocks.models import Content

register = template.Library()


@register.simple_tag
def rich_content_block(key):
    obj = Content.get_content_by_key(key=key)

    if obj:
        return obj.content
    else:
        return 'Content object does not exist.'
