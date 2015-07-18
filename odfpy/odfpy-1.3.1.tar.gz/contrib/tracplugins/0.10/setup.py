# -*- coding: utf-8 -*-
# Copyright (C) 2007 Søren Roug, European Environment Agency
#
# This is free software.  You may redistribute it under the terms
# of the Apache license and the GNU General Public License Version
# 2 or at your option any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
#
# Contributor(s):
#

from setuptools import setup

PACKAGE = 'OdfConversion'
VERSION = '0.1'

setup(name='OdfConversion',
      version='0.1',
      packages=['odfpreview','odftohtml'],
      author='Soren Roug',
      author_email='soren.roug@eea.europa.eu',
      description='A plugin for viewing ODF documents as HTML',
      url='http://trac-hacks.org/wiki/OdfConversion',
      entry_points={'trac.plugins': ['odfpreview.odfpreview=odfpreview.odfpreview',
       'odftohtml.odftohtml=odftohtml.odftohtml']})
