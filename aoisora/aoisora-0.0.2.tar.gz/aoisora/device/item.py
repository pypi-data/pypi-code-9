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

from PyQt4 import QtGui
from PyQt4 import QtCore

from .mixin import DeviceMixin


class DeviceItem(DeviceMixin, QtGui.QTreeWidgetItem):
    interface_name = 'org.bluez.Device1'
    DEVICE_STATUSES = 'Paired', 'Connected', 'Trusted', 'Blocked'

    def __init__(self, *args, **kwargs):
        self._path = kwargs.pop('path')
        self._dev = kwargs.pop('dev')
        super(DeviceItem, self).__init__(*args, **kwargs)

    def data(self, column, role):
        if role == QtCore.Qt.DisplayRole:  # labels
            if column == 0:
                try:
                    name = self.getProperty('Name')
                except dbus.exceptions.DBusException:
                    name = self.getProperty('Address')
                return str(name)
            elif column == 1:
                return ' & '.join(filter(
                    self.getProperty, self.DEVICE_STATUSES))
        elif role == QtCore.Qt.DecorationRole:  # icon
            if column == 0:
                return QtGui.QIcon.fromTheme(self.getProperty('Icon'))
        super(DeviceItem, self).data(column, role)

    def connect(self):
        self.interface.Connect()

    def disconnect(self):
        self.interface.Disconnect()

    def pair(self):
        self.interface.Pair()

    def trusted(self):
        self.setProperty('Trusted', not self.getProperty('Trusted'))

    def blocked(self):
        self.setProperty('Blocked', not self.getProperty('Blocked'))
