from jinja2 import Environment, FileSystemLoader

from okapi.templatetags import filters


class TemplateSettings(object):
    env = None

    def set_env(self, paths):
        self.env = Environment(loader=FileSystemLoader(paths))
        self.env.filters.update(filters)
