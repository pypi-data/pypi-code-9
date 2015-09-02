__author__ = 'marcos.medeiros'

from django import template
from django.utils.safestring import mark_safe
from django.template import loader, Context
from django.utils.html import escape
from rapid.views import registry, ModelData
from rapid import filters

register = template.Library()

_base = 'rapid/list/'

@register.inclusion_tag(_base+'field_header.html')
def field_header(field):
    return {'f': field}

@register.inclusion_tag(_base+'pagination.html', takes_context=True)
def pagination(context):
    return context

@register.inclusion_tag(_base+'show_value.html')
def show_value(val, val_data):
    return {'val': val, 'val_data': val_data}

@register.inclusion_tag(_base+'instance_actions.html')
def instance_actions(instance):
    return {'o': instance}
