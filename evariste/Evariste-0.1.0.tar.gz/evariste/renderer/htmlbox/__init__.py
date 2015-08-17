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

"""Render tree as an HTML (body) page, with CSS"""

import os
import pkg_resources

from evariste import utils
from evariste.renderer.html import HTMLRenderer

class HTMLBoxRenderer(HTMLRenderer):
    """Render tree as an HTML div (without the `<div>` tags)."""
    # pylint: disable=too-few-public-methods

    keyword = "htmlbox"
    depends = {
        'required': {
            'misc': [
                'copy',
            ],
        },
        'suggested': {
            'renderer.htmlbox.target': [
                'image',
                'default',
                ],
            'renderer.htmlbox.readme': [
                'html',
                ],
            },
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.environment.filters['labelize'] = self._labelize
        if 'copy_htmlbox' not in self.shared.setup['misc.copy']:
            self.shared.setup['misc.copy']['copy_htmlbox'] = (
                pkg_resources.resource_filename(
                    self.__class__.__module__,
                    os.path.join("data", "static"),
                    ),
                utils.expand_path(self.local.setup['staticdir']),
                )

    @staticmethod
    def _labelize(string):
        """Return a label, given a string.

        The label starts with alphabetical ascii characters, followed by
        digits. Two different strings have different hashes.
        """
        return "label" + str(hash(string))

    def _templatedirs(self):
        yield from super()._templatedirs()
        yield pkg_resources.resource_filename(
            "evariste.renderer.html",
            os.path.join("data", "templates"),
            )
