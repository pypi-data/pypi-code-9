# -*- coding: utf-8 -*-
__author__ = 'Alex Bo'
__email__ = 'bosha@the-bosha.ru'

class BaseTemplater:

    instance = None
    env = None
    template_name = None

    def __init__(self, instance):
        self.instance = instance
        self.template_name = instance.template_name

    def render(self, **kwargs):
        raise NotImplementedError(
            "render should be implemented in %s" % (self.__class__.__name__)
        )
