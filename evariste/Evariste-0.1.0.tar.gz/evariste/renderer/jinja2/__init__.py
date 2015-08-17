# Copyright Louis Paternault 2015
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Abstract class for jinja2 renderers."""

import jinja2
import os
import pkg_resources
import pathlib
import textwrap

from evariste import utils
from evariste.renderer.dest import DestRenderer
from evariste.renderer.jinja2.readme import Jinja2ReadmeRenderer
from evariste.renderer.jinja2.target import Jinja2TargetRenderer

class JinjaRenderer(DestRenderer):
    """Abstract class for jinja2 renderers."""
    # pylint: disable=too-few-public-methods

    extension = None
    subplugins = {
        "target": Jinja2TargetRenderer,
        "readme": Jinja2ReadmeRenderer,
        }

    def __init__(self, shared):
        super().__init__(shared)

        self.environment = jinja2.Environment(
            loader=jinja2.FileSystemLoader(
                self._templatedirs(),
            )
        )
        self.environment.filters['basename'] = os.path.basename
        self.environment.filters['yesno'] = utils.yesno

    def _templatedirs(self):
        """Iterator over the directories in which templates may exist.

        - Directories are returned as strings;
        - directories may not exist.
        """
        if self.local.setup['templatedirs'] is not None:
            yield from utils.expand_path(self.local.setup['templatedirs']).split()
        yield pkg_resources.resource_filename( #pylint: disable=no-member
            self.__class__.__module__,
            os.path.join("data", "templates")
            )
        yield from [
            os.path.join(utils.expand_path(path), "templates")
            for path
            in [".evariste", "~/.config/evariste", "~/.evariste", "/usr/share/evariste"]
            ]

    def _template(self):
        """Return the name of the template to use."""
        if self.local.setup['template'] is not None:
            return self.local.setup['template']
        return "tree.{}".format(self.extension)

    def render(self, tree):
        return self._render(
            tree=tree,
            template=self._template(),
            context={
                'destdir': pathlib.Path(self.destdir),
                'shared': self.shared,
                'local': self.local,
                'render': self._render,
                'render_download': self._render_download,
                'render_readme': self._render_readme,
                'render_file': self._render_file,
                'render_directory': self._render_directory,
                'render_template': self._render_template,
                },
            )

    @jinja2.contextfunction
    def _render(self, context, tree, template):
        """Render the tree, using given template (or template list)."""
        if isinstance(context, dict):
            context['tree'] = tree
        else:
            context.vars['tree'] = tree
        if tree.is_file() and tree.report.success:
            utils.copy(
                (tree.root.from_fs / tree.report.target).as_posix(),
                (context['destdir'] / tree.report.target).as_posix(),
                )
        return textwrap.indent(
            self.environment.get_or_select_template(template).render(context),
            "  ",
            )

    @jinja2.contextfunction
    def _render_directory(self, context, tree):
        """Render ``tree``, which is a :class:`tree.Directory`, as HTML."""
        return self._render(context, tree, "tree_directory.{}".format(self.extension))

    @jinja2.contextfunction
    def _render_file(self, context, tree):
        """Render ``tree``, which is a :class:`tree.File`."""
        return self.shared.builder.plugins.match_plugin(
            "{}.target".format(self.plugin_id), tree
            ).render(tree, context)

    @jinja2.contextfunction
    def _render_download(self, context, tree):
        """Render the code downloading the archive."""
        path = tree.make_archive(context["destdir"])
        context.vars['href'] = path.as_posix()
        context.vars['content'] = path.name
        return self.environment.get_template("download.{}".format(self.extension)).render(context) # pylint: disable=no-member

    @jinja2.contextfunction
    def _render_readme(self, context, tree):
        """Find the readme of tree, and returns the corresponding code."""
        # pylint: disable=unused-argument
        readme_plugins = self.shared.builder.plugins.get_plugin_type(
            "{}.readme".format(self.plugin_id)
            ).values()
        readme = tree.render_readme(readme_plugins, context)
        if readme:
            return readme
        return ""

    @jinja2.contextfunction
    def _render_template(self, context, template):
        """Render template given in argument."""
        with open(template) as file:
            return self.environment.from_string(file.read()).render(context)
