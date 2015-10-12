# copyright 2006-2011 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr/ -- mailto:contact@logilab.fr
#
# This file is part of logilab-mtconverter.
#
# logilab-mtconverter is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation, either version 2.1 of the License, or (at your
# option) any later version.
#
# logilab-mtconverter is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License
# for more details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with logilab-mtconverter. If not, see <http://www.gnu.org/licenses/>.

from six import binary_type

from html2text import html2text

from logilab.mtconverter.transform import Transform


class html_to_formatted_text(Transform):
    """transforms html to formatted plain text"""

    name = "html_to_text"
    inputs  = ("text/html",)
    output = "text/plain"


    def _convert(self, trdata):
        if isinstance(trdata.data, binary_type):
            data = trdata.data.decode(trdata.encoding)
        else:
            data = trdata.data
        return html2text(data).encode(trdata.encoding)
