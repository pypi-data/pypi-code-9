import jinja2
import os
from .templates import classpath_template, project_template


def _render_project_file(project_name):
    template = jinja2.Template(project_template)
    return template.render(project_name=project_name)


def _write_classpath_file(destination):
    with open(os.path.join(destination, ".classpath"), "w") as f:
        f.write(classpath_template)


def _write_project_file(destination, project_name):
    with open(os.path.join(destination, ".project"), "w") as f:
        f.write(_render_project_file(project_name))


def write_metadata_files(destination, project_name):
    if destination is None:
        destination = project_name
    _write_classpath_file(destination)
    _write_project_file(destination, project_name)