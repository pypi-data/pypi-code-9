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

from expression import CachedExpression

class Function(CachedExpression):
    def __init__(self, fname, derivatives=None):
        super(Function, self).__init__()
        self.fname = fname
        self.derivatives = derivatives
        if self.derivatives is None:
            self.derivatives = []
        self.derivatives.sort()

    def _bind(self, binding):
        repr_self = repr(self)
        if repr_self in binding:
            return binding[repr_self]
        else:
            return self

    def _differentiate(self, variable):
        return Function(self.fname, self.derivatives+[variable])

    def __eq__(self, other):
        return self.fname == other.fname and \
                self.derivatives == other.derivatives

    def __repr__(self):
        if len(self.derivatives) == 0:
            return self.fname

        dvars = list(set(self.derivatives))
        dvars.sort()
        ddata = [(self.derivatives.count(dvar), dvar) for dvar in dvars]
        dstr = ''.join(['d%d%s'%(_[0], _[1]) if _[0] > 1 else 'd%s'%(_[1])
                        for _ in ddata])
        dfstr = 'd%d%s'%(len(self.derivatives), self.fname) \
                    if len(self.derivatives) > 1 else 'd%s'%(self.fname)
        return '%s_%s'%(dfstr, dstr)
