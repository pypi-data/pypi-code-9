from django.conf.urls import url, patterns
from django.views.generic.base import TemplateView

from djangocms_contact import views

urlpatterns = patterns('',
    url(r'^$', views.ContactView.as_view(), name='contact'),
    url(r'^success/$',
        TemplateView.as_view(template_name='djangocms_contact/success.html'),
        name='success'),
)
