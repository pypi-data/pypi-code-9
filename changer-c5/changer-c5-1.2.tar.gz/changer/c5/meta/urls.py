from django.conf.urls import patterns, url
from django.views.generic import TemplateView

urlpatterns = patterns(
    url(r'^robots\.txt$',
        TemplateView.as_view(template_name='robots.txt'),
        name="robots"),
    url(r'^humans\.txt',
        TemplateView.as_view(template_name='humans.txt')),
)
