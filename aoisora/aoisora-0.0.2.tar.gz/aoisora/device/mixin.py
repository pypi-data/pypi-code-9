# Copyright (C) 2015 Okami, okami@fuzetsu.info

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.

import dbus


class DeviceMixin(object):
    interface_name = None

    _interface = None
    _properties = None

    @property
    def interface(self):
        if not self._interface:
            self._interface = dbus.Interface(self._dev, self.interface_name)
        return self._interface

    @property
    def properties(self):
        if not self._properties:
            self._properties = dbus.Interface(
                self._dev, 'org.freedesktop.DBus.Properties')
        return self._properties

    def getProperty(self, key):
        return self.properties.Get(self.interface_name, key)

    def setProperty(self, key, value):
        self.properties.Set(self.interface_name, key, value)
