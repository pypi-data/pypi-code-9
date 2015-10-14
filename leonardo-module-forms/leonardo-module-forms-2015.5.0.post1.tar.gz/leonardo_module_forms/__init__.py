
from django.apps import AppConfig

from .widget import *


default_app_config = 'leonardo_module_forms.FormConfig'


class Default(object):

    optgroup = ('Forms')

    @property
    def apps(self):
        INSTALLED_APPS = []
        try:
            import django_remote_forms # noqa
        except ImportError:
            pass
        else:
            INSTALLED_APPS += ['django_remote_forms']

        return INSTALLED_APPS + [
            'crispy_forms',
            'form_designer',
            'leonardo_module_forms',
        ]

    @property
    def widgets(self):
        return [
            FormWidget,
        ]


class FormConfig(AppConfig):
    name = 'leonardo_module_forms'
    verbose_name = "Module Forms"

    conf = Default()

default = Default()
