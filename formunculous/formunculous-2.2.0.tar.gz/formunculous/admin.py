from django.contrib import admin
from django.conf.urls.defaults import *
from formunculous.models import Form
from django.utils.functional import lazy
from django.core.urlresolvers import reverse

reverse_lazy = lazy(reverse, unicode)

class FormAdmin(admin.ModelAdmin):
    """
       This "Admin Model" is used to shim proper URLs for administering
       formunculous.
    """

    def get_urls(self):
        urls = patterns('django.views.generic.simple',
                        url(r'^$', 'redirect_to', 
                            {'url': reverse_lazy('builder-index')},
                            name="formunculous_applicationdefinition_changelist"),
                        
                        url(r'^add/$', 'redirect_to', 
                            {'url': reverse_lazy('builder-add-ad')},
                            name="formunculous_applicationdefinition_add"),
                        )
        return urls
                        
admin.site.register(Form, FormAdmin)
