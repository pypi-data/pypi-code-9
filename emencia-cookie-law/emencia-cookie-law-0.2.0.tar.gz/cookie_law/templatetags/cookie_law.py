"""
Cookie law tags
"""
import warnings

from django.conf import settings
from django import template
from django.template.loader import render_to_string


register = template.Library()


#class CookielawBanner(InclusionTag):
    #"""
    #Displays cookie law banner only if user has not dismissed it yet.
    #"""

    #template = 'cookielaw/banner.html'

    #def render_tag(self, context, **kwargs):
        #template_filename = self.get_template(context, **kwargs)

        #if 'request' not in context:
            #warnings.warn('No request object in context. '
                          #'Are you sure you have django.core.context_processors.request enabled?')

        #if context['request'].COOKIES.get('cookielaw_accepted', False):
            #return ''

        #data = self.get_context(context, **kwargs)
        #return render_to_string(template_filename, data, context_instance=context)

#register.tag(CookielawBanner)



class CookieLawTag(template.Node):
    def __init__(self):
        pass
        
    def render(self, context):
        cookie_name = getattr(settings, 'COOKIELAW_COOKIE_NAME', 'emencia_cookie_law')
        banner_template = getattr(settings, 'COOKIELAW_TEMPLATE', 'cookie_law/banner.html')
        if 'request' not in context:
            warnings.warn("Request object is required in template context. Add 'django.core.context_processors.request' to your template context processor setting.")
        elif not context['request'].COOKIES.get(cookie_name, False):
            return render_to_string(banner_template, {}, context_instance=context)
    
        return ''

@register.tag(name="cookie_law_banner")
def do_cookielaw_tag(parser, token):
    return CookieLawTag()
