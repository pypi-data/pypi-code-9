import os
import time
import shutil

from paste.script import templates
from paste.script.templates import var


class PyTemplate(templates.Template):

    _template_dir = 'templates'
    egg_plugins = ['python_template']
    summary = 'A standard, modern Python project'
    required_templates = []
    use_cheetah = True

    vars = [
        var('module_name', 'Module name (like "Project Issue")',
            default='My Module'),
        var('description', 'One-line description of the module'),
        var('keywords', 'Space-separated keywords/tags'),
        var('author', 'Author name', default=os.getlogin()),
        var('author_email', 'Author email'),
        var('url', 'URL of homepage'),
    ]

    def pre(self, command, output_dir, vars):
        """
        Called before template is applied.
        """
        # import pdb;pdb.set_trace()
        vars['license_name'] = 'Apache'
        vars['year'] = time.strftime('%Y', time.localtime())

    def post(self, command, output_dir, vars):
        template_dir = self.template_dir()
        current_dir = os.path.join(output_dir, vars['package'])

        # apparently .dotfiles are not copied by Paster
        hidden_files = ['.gitignore']
        for hf in hidden_files:
            shutil.copyfile(
                os.path.join(template_dir, hf),
                os.path.join(output_dir, hf)
            )
