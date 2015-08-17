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

"""Set of plugins testing plugin dependency, and enabling/disabling plugins.

Does nothing, but printing stuff to standard output.
"""

from datetime import datetime
import os
import pathlib

from evariste.misc import Misc

class TestPlugin(Misc):
    """Generic test plugin"""

    pass

################################################################################
# Dummy plugins

class Foo(TestPlugin):
    keyword = "foo"

class Bar(TestPlugin):
    keyword = "bar"

################################################################################
# Default / Required plugins

class Required(TestPlugin):
    keyword = "required"
    required = True

class Default(TestPlugin):
    keyword = "default"
    default = True

################################################################################
# Dependencies : First simple plugins

class DependsRequired(TestPlugin):
    keyword = "dependsrequired"
    depends = {
        'required': {
            'misc': ['foo'],
        },
    }

class DependsOptional(TestPlugin):
    keyword = "dependsoptional"
    depends = {
        'suggested': {
            'misc': ['foo'],
        },
    }

class DependsBoth(TestPlugin):
    keyword = "dependsboth"
    depends = {
        'required': {
            'misc': ['foo'],
        },
        'suggested': {
            'misc': ['bar'],
        },
    }

################################################################################
# Dependecies : Recursive dependency

class DependsOptionalOptional(TestPlugin):
    keyword = "dependsoptionaloptional"
    depends = {
        'suggested': {
            'misc': ['dependsoptional'],
        },
    }

class DependsOptionalRequired(TestPlugin):
    keyword = "dependsoptionalrequired"
    depends = {
        'suggested': {
            'misc': ['dependsrequired'],
        },
    }

class DependsRequiredRequired(TestPlugin):
    keyword = "dependsrequiredrequired"
    depends = {
        'required': {
            'misc': ['dependsrequired'],
        },
    }

class DependsRequiredOptional(TestPlugin):
    keyword = "dependsrequiredoptional"
    depends = {
        'required': {
            'misc': ['dependsoptional'],
        },
    }
