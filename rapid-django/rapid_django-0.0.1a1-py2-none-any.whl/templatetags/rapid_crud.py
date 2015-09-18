__author__ = 'marcos.medeiros'

from django import template
from django.template import loader, Context
import random
from django.utils.safestring import mark_safe

register = template.Library()

@register.inclusion_tag('rapid/bare/list.html', takes_context=True)
def crud_list(context):
    return context

@register.inclusion_tag('rapid/bare/select.html', takes_context=True)
def crud_select(context):
    return context

@register.inclusion_tag('rapid/bare/detail.html', takes_context=True)
def crud_view(context):
    return context

@register.inclusion_tag('rapid/bare/update.html', takes_context=True)
def crud_update(context):
    return context

@register.inclusion_tag('rapid/bare/create.html', takes_context=True)
def crud_create(context):
    return context

@register.inclusion_tag('rapid/bare/delete.html', takes_context=True)
def crud_delete(context):
    return context

def random_name():
    s = "abcdefghijklmnopqrustuvwxyz"
    return "".join([random.choice(s) for x in xrange(30)])

def render_to_javascript_string(template, context={}):
    t = loader.get_template(template)
    c = Context(context)
    str = t.render(c)
    str = str.replace("\"", "\\\"")
    str = str.replace("\n", "\\n")
    return mark_safe(str)

@register.inclusion_tag('rapid/overlay/register.html')
def register_overlay():
    overlay_text = render_to_javascript_string('rapid/overlay/text.html')
    return {'overlay_text': overlay_text}

@register.inclusion_tag('rapid/overlay/call.html')
def overlay(target_url, on_commit=None, on_close=None):
    if not on_commit:
        on_commit = 'function(){}'
    if not on_close:
        on_close = 'function(){}'
    return {
        'target_url': target_url,
        'on_commit': on_commit,
        'on_close': on_close,
        }
