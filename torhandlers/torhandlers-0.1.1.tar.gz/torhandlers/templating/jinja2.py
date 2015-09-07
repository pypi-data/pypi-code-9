# -*- coding: utf-8 -*-
__author__ = 'Alex Bo'
__email__ = 'bosha@the-bosha.ru'

from torhandlers.base import HTTPError
from torhandlers.templating.base import BaseTemplater
from torhandlers.templating.exceptions import TemplatingException

class Jinja2Templater(BaseTemplater):

    def render(self, **kwargs):

        jinja2_env = self.instance.settings['jinja2_env']
        if not jinja2_env:
            raise TemplatingException(
                "To use Jinja2Templater you should define jinja2 setings in"
                "global application settings dict"
            )

        try:
            template = jinja2_env.get_template(self.template_name)
        except Exception as e:
            raise HTTPError(404)

        kwargs.update(self.instance.get_template_namespace())
        jinja2_env.globals['static_url'] = self.instance.static_url
        jinja2_env.globals['xsrf_token'] = self.instance.xsrf_token
        jinja2_env.globals['xsrf_form_html'] = self.instance.xsrf_form_html
        self.instance.write(template.render(kwargs))
