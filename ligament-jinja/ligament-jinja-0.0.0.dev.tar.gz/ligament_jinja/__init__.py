""" Basic Jinja2 templating for the `ligament` task automator"""
import os
import jinja2
from ligament.buildtarget import BuildTarget

from ligament.helpers import mkdir_recursive

class SimpleJinja(BuildTarget):

    def __init__(self, input_file="", output_file="", **kwargs):
        BuildTarget.__init__(self, **kwargs)

        self.input_file  = input_file
        self.output_file = output_file

        self.jinja_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(
                os.path.dirname(input_file)))

        self.input_basename = os.path.basename(self.input_file)

        self.file_watch_targets = [os.path.abspath(input_file)]

    def build(self, **kwargs):

        directory = os.path.dirname(self.output_file)
        if directory != "" and not os.path.exists(directory):
            mkdir_recursive(os.path.dirname(self.output_file))

        template = self.jinja_env.get_template(self.input_basename)
        html = template.render(
            **kwargs
        )

        with open(self.output_file, 'w') as template_output:
            template_output.write(html)

        return html
