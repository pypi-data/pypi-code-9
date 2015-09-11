# Copyright 2014 Alex Orange
# 
# This file is part of LDB Algebra.
# 
# LDB Algebra is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# LDB Algebra is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
# 
# You should have received a copy of the GNU Affero General Public License
# along with LDB Algebra.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import absolute_import

import weakref

class VariableExistsError(Exception):
    pass

class ExpressionManager(object):
    def __init__(self):
        self.variable_dict = weakref.WeakValueDictionary()

    def register_variable(self, name, obj):
        if name in self.variable_dict:
            raise VariableExistsError

        self.variable_dict[name] = obj

    def get_variable(self, name):
        return self.variable_dict[name]

    def has_variable(self, name):
        return name in self.variable_dict
