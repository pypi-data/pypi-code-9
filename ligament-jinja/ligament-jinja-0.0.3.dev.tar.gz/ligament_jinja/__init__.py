""" Basic Jinja2 templating for the `ligament` task automator"""
import os
import jinja2
from ligament.buildtarget import BuildTarget

from ligament.helpers import mkdir_recursive

class SimpleJinja(BuildTarget):

    def __init__(self, template_file="", filters={}, **kwargs):
        BuildTarget.__init__(self, **kwargs)

        self.template_file  = template_file
        self.jinja_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(
                os.path.dirname(self.template_file)))

        self.jinja_env.filters = filters

        self.input_basename = os.path.basename(self.template_file)

        self.file_watch_targets = [os.path.abspath(self.template_file)]

    def build(self, output_file=None, **kwargs):

        if output_file is not None:
            directory = os.path.dirname(output_file)
            if directory != "" and not os.path.exists(directory):
                mkdir_recursive(os.path.dirname(output_file))

        template = self.jinja_env.get_template(self.input_basename)
        html = template.render(
            **kwargs
        )

        if output_file is not None:
            with open(output_file, 'w') as template_output:
                template_output.write(html)

        return html
