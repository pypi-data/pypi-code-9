from jinja2 import Environment, FileSystemLoader
import os, shutil
from . import Output

class WebsiteOutput(Output):
    template = None
    environment = None

    def __init__(self, themepath):
        self.themepath = themepath

        self.environment = Environment( loader=FileSystemLoader(self.themepath))
        self.environment.filters['format_date'] = lambda date: date.strftime("%d.%m.%Y %H:%M")
        self.environment.filters['format_tag'] = lambda *args, **kwargs: args[0]
        self.environment.filters['intro'] = lambda content: "%s</div>" % content.split('</div>')[0]

        self.environment.globals['assets'] = lambda *x: x[0]

        self.template = self.environment.get_template('theme.html')

    @property
    def site(self):
        return {
            'twitter': 'tspycher',
        }

    @property
    def theme(self):
        return {"social":None}

    @property
    def header_meta(self):
        return ""

    def render(self, site, **kwargs):
        return self.template.render(**dict({
            "header_meta": self.header_meta,
            "site": site,
            "theme": self.theme,
            "is_login": False,
            "is_home": False,
            "is_tag": False
        }.items() + kwargs.items()) )

