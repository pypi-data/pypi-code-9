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


"""Text rendere: print report on terminal."""

import unidecode
import sys

from evariste.renderer import Renderer
from evariste.utils import yesno

class TextRenderer(Renderer):
    """Text renderer: print report on terminal."""

    keyword = 'text'
    default_setup = {
        'color': "auto",
        'ascii': False,
        }

    def render(self, tree):

        # Option 'ascii'
        if yesno(self.local.setup['ascii']):
            def asciiprint(text):
                """Convert argument to ascii, and print it."""
                print(unidecode.unidecode(text))
            print_function = asciiprint
        else:
            print_function = print

        # Option 'color'
        color = self.local.setup['color']
        if color.lower() == 'auto':
            color = sys.stdout.isatty() # pylint: disable=no-member
        color = yesno(color)

        # Render
        tree.pprint(
            report=True,
            color=color,
            print_function=print_function,
            )
