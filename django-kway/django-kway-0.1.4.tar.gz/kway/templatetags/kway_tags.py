# -*- coding: utf-8 -*-

from django import template
from django.template.defaultfilters import stringfilter

from kway import kgetimage, kgettext


register = template.Library()


@register.simple_tag(takes_context = False)
def kimage(key, *args, **kwargs):
    
    value = kgetimage(key, *args, **kwargs)
    
    return value


@register.simple_tag(takes_context = False)
def ktext(key, key_plural = None, count = None, *args, **kwargs):
    
    value = kgettext(key, key_plural, count, *args, **kwargs)
    
    return value
    
    
@register.simple_tag(takes_context = False)
def ktrans(key, key_plural = None, count = None, *args, **kwargs):
    
    value = kgettext(key, key_plural, count, *args, **kwargs)
    
    return value
    
    