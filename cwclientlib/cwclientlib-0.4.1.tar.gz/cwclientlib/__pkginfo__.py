# pylint: disable=W0622
# copyright 2014-2015 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr/ -- mailto:contact@logilab.fr
#
# This file is part of cwclientlib.
#
# cwclientlib is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation, either version 2.1 of the License, or (at your
# option) any later version.
#
# cwclientlib is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License
# for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with cwclientlib. If not, see <http://www.gnu.org/licenses/>.

"""cwclientlib application packaging information"""

import sys

modname = 'cwclientlib'
distname = 'cwclientlib'

numversion = (0, 4, 1)
version = '.'.join(str(num) for num in numversion)

license = 'LGPL'
author = 'LOGILAB S.A. (Paris, FRANCE)'
author_email = 'contact@logilab.fr'
description = 'A Python library to easily build CubicWeb clients'
web = 'http://www.cubicweb.org/project/%s' % distname

cliversion = ''
if sys.version_info[0] > 2:
    cliversion = '3'
console_scripts = ['cwrql{0}=cwclientlib.cwrql:main'.format(cliversion),
                   'cwget{0}=cwclientlib.cwget:main'.format(cliversion),
                   'cwshell{0}=cwclientlib.cwshell:main'.format(cliversion),
                   ]

install_requires = ['requests >= 2', 'six']
extras_require = {'kerberos': ['requests-kerberos'],
                  'yaml': ['PyYAML'],
                  }
test_suite = 'cwclientlib.test'
tests_require = ['cubicweb >= 3.20',
                 'cubicweb-signedrequest',
                 'cubicweb-rqlcontroller',
                 'cubicweb-file',
                 'twisted', 'pyramid', 'PyYAML',
                 'requests', 'requests-kerberos',
                 ]

classifiers = [
    'Environment :: Web Environment',
    'Framework :: CubicWeb',
    'Programming Language :: Python',
    ]
