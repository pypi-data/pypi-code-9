from django.views.generic.base import TemplateView


class DisabledView(TemplateView):
    template_name = 'ipapi/disabled.html'
