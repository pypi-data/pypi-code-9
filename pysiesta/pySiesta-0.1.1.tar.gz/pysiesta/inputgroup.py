# Copyright (C) 2014 Ezequiel Castillo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from keys import KeyContainer, BaseKey, BlockKey


class GroupContainer(list):

    def update_group(self, group=None, keyword=None):
        if group not in self:
            self.append(InputGroup(group))

    def add_key_to_group(self, keyword, group):
        idx = self.get_index(group)
        self[idx].addKey(keyword)

    def get_index(self, group=None):
        for i, g in enumerate(self):
            if g.name == group:
                return i

    def get_string_from_all_groups(self):
        s = ''
        for g in self:
            s += g._write_group()
        return s

    def __contains__(self, group):
        return group in map(lambda g: g.name, self)

    def __repr__(self):
        return '[' + ''.join(['%i:%s' % (i, g.name) for i, g in enumerate(self) ]) + ']'


class InputGroup(KeyContainer):

    def __init__(self, name=None):

        if name is not None:
            self.name = name

    def _write_group(self):
        s = self.name
        spacer = self._get_max_spacer()
        for k in self:
            if isinstance(k, BlockKey):
                s += repr(k)
            else:
                cs = spacer - len(k.name) + 2
                s += k.name + ' ' * cs + k.value + '\n'
        s += '\n'
        return s

    def _get_max_spacer(self):
        l = [len(k.name) for k in self if not isinstance(k, BlockKey)]
        if l:
            return max(l)

    # WARNING: no self argument, 'cause it's kind of staticmethod.
    @staticmethod
    def _sort_order(k):
        if isinstance(k, BlockKey):
            return 1
        else:
            return 0

    def __repr__(self):
        return self.name

    def __setattr__(self, attr, value):
        if attr == 'name':
            self.__dict__[attr] = value
        elif isinstance(self.__dict__[attr], BaseKey):
            self.__dict__[attr].value = value

    def __getitem__(self, index):
        return sorted([k for k in self.__dict__.values() if not k == self.name], key=InputGroup._sort_order)[index]
