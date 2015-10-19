# -*- coding: utf-8 -*-
from jinja2 import Template

import os
from apiary.helpers.javascript_helper import escape_javascript


class Preview(object):
    PREVIEW_TEMPLATE_PATH = os.path.dirname(os.path.abspath(__file__)) + '/../file_templates/preview.py'

    def __init__(self, **kwargs):
        self.options = kwargs
        self.template = None

    def execute(self):
        print(self.options)
        if self.options['server']:
            self.server()
        else:
            self.show()

    def server(self):
        print('todo 1')

    def show(self):
        self.generate_static()

    def generate_static(self):
        preview_string = self.generate()

        with open(self.options['output'], 'w') as f:
            f.write(preview_string.encode('utf-8'))

    def generate(self):
        self.load_preview_template()

        # data = {
        # title: File.basename(@options.path, '.*'),
        # blueprint: load_blueprint
        # }

        return self.template.render(title="API", magic=escape_javascript(self.load_blueprint()).decode('utf-8'))

    def load_preview_template(self):
        template_file = open(Preview.PREVIEW_TEMPLATE_PATH, 'r')
        template_string = template_file.read()
        self.template = Template(template_string)
        template_file.close()

    def load_blueprint(self):
        f = open(self.options['path'], 'r')
        blueprint = f.read()
        f.close()
        return blueprint
