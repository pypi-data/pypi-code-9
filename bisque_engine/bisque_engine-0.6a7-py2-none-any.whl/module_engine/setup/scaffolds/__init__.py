from pyramid.scaffolds import PyramidTemplate
from textwrap import dedent

class PythonModuleTemplate(PyramidTemplate):
    _template_dir = 'python_module'
    summary = 'Create a basic python bisque module '
    quiet = True
    def post(self, command, output_dir, vars): # pragma: no cover
        pass
    def out(self, msg):
        pass

class MatlabModuleTemplate(PyramidTemplate):
    _template_dir = 'matlab_module'
    summary = 'Create a basic python bisque module '
    quiet = True
    def post(self, command, output_dir, vars): # pragma: no cover
        pass
    def out(self, msg):
        pass

