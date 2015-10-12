# copyright 2006-2012 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
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
"""mtconverter packaging information"""

modname = "mtconverter"
distname = "logilab-mtconverter"
subpackage_of = 'logilab'

numversion = (0, 9, 0)
version = '.'.join([str(num) for num in numversion])

license = 'LGPL'
web = "http://www.logilab.org/project/%s" % distname
mailinglist = "mailto://python-projects@lists.logilab.org"

description = "a library to convert from a MIME type to another"
author = "Sylvain Thenault"
author_email = "contact@logilab.fr"

install_requires = [
    'setuptools',
    'six >= 1.4.0',
    'logilab-common',
    'lxml',
    'html2text',
    ]
