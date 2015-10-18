# coding: utf-8

from django.apps import AppConfig


class DefaultConfig(AppConfig):
    name = 'sticky_files'
    verbose_name = 'Sticky files'

    def ready(self):
        pass
