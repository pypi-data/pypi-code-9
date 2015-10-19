# -*- coding: utf-8 -*-
from jinja2 import Template

import os
from apiary.helpers.javascript_helper import escape_javascript


class Preview:
    PREVIEW_TEMPLATE_PATH = os.path.dirname(os.path.abspath(__file__)) + '/../file_templates/preview.j2'

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

        # File.open(preview_path, 'w') do |file|
        # file.write preview_string
        # file.flush
        # @options.output ? write_generated_path(file.path, @options.output) : open_generated_page(file.path)

        f = open(self.options['output'], 'w')
        f.write(preview_string)
        f.close

    def generate(self):
        template = self.load_preview_template()

        # data = {
        # title: File.basename(@options.path, '.*'),
        # blueprint: load_blueprint
        # }

        return self.template.render(title="API", magic=escape_javascript(self.load_blueprint()))

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
