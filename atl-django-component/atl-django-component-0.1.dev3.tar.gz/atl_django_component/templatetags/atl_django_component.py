# encoding=utf-8
from django import template
from pydoc import locate
from django.conf import settings

register = template.Library()


@register.inclusion_tag('atl_django_component/component.html', takes_context=True)
def show_atl_component(context, component, template_name=None):
    component_context = {}
    component_context['SEKIZAI_CONTENT_HOLDER'] = context['SEKIZAI_CONTENT_HOLDER']
    component_context['debug'] = settings.DEBUG
    if template_name and template_name in component.template.keys():
        template = component.template[template_name]
    else:
        template = component.template['default']
    component_context['atl_component'] = component
    component_context['atl_component_template'] = template
    component_context['atl_component_view'] = template_name
    return component_context

@register.inclusion_tag('atl_django_component/component.html', takes_context=True)
def create_and_show_atl_component(context, component_class, data_provider=None, template_name=None, **kwargs):
    component = locate(component_class)(data_provider, **kwargs)
    component_context = show_atl_component(context, component, template_name)
    return component_context