# coding=utf-8
"""PickleJar is a python module that allows you to work with multiple pickles while reading/writing them to a single
file/jar.  You can load the entire jar into memory or work with pickles individually inside the jar."""
# Copyright (C) 2015 Jesse Almanrode
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU Lesser General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU Lesser General Public License for more details.
#
#     You should have received a copy of the GNU Lesser General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Imports
import os
import dill


class Jar(object):
    """A file containing multiple pickle objects

    - **parameters** and **return types**::

        :param filepath: Path to the file
        :return: Jar object
    """
    def __init__(self, filepath):
        self.jar = os.path.abspath(filepath)

    def dump(self):
        """Dumps all the pickles out of the jar (loading them to memory)

        - **parameters** and **return types**::

            :return: List of de-pickled objects
        """
        _pickles = []
        _jar = open(self.jar, 'rb')
        while True:
            try:
                _pickles.append(dill.load(_jar))
            except EOFError:
                break
        _jar.close()
        if len(_pickles) == 1:
            return _pickles[0]
        else:
            return _pickles

    def collect(self, pickles, newjar=False):
        """Pickle an item or list of items to a file.

        - **parameters** and **return types**::

            :param pickles: Item or list of items to pickle
            :param newjar: Start a new jar (default = False)
            :return: None
        """
        if newjar:
            _jar = open(self.jar, 'wb')
        else:
            _jar = open(self.jar, 'ab')
        if type(pickles) is list:
            for pkle in pickles:
                dill.dump(pkle, _jar, dill.HIGHEST_PROTOCOL)
        else:
            dill.dump(pickles, _jar, dill.HIGHEST_PROTOCOL)
        _jar.close()
        return None
