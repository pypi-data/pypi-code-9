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

from .item import DeviceItem
from .mixin import DeviceMixin
from .thread import DeviceThread


class DeviceTreeWidget(DeviceMixin, QtGui.QWidget):
    interface_name = 'org.bluez.Adapter1'

    def __init__(self, *args, **kwargs):
        self._dev = kwargs.pop('dev')
        super(DeviceTreeWidget, self).__init__(*args, **kwargs)

        self._thread = DeviceThread()
        self._thread.start()

        self._list = QtGui.QTreeWidget()
        self._list.setHeaderLabels(('Device', 'Status'))
        self._list.setColumnWidth(0, 400)
        self._list.setSortingEnabled(True)
        self._list.sortItems(0, QtCore.Qt.AscendingOrder)
        self._list.currentItemChanged.connect(self._on_item_changed)

        self._connect = QtGui.QPushButton('Connect')
        self._connect.clicked.connect(self._on_connect)
        self._disconnect = QtGui.QPushButton('Disconnect')
        self._disconnect.clicked.connect(self._on_disconnect)
        self._pair = QtGui.QPushButton('Pair')
        self._pair.clicked.connect(self._on_pair)
        self._remove = QtGui.QPushButton('Remove')
        self._remove.clicked.connect(self._on_remove)
        self._trusted = QtGui.QCheckBox('Trusted')
        self._trusted.clicked.connect(self._on_trusted)
        self._blocked = QtGui.QCheckBox('Blocked')
        self._blocked.clicked.connect(self._on_blocked)

        grid = QtGui.QGridLayout()
        grid.setRowStretch(3, 0)
        grid.setSpacing(10)

        grid.addWidget(self._list, 0, 0, 7, 1)
        grid.addWidget(self._connect, 0, 1)
        grid.addWidget(self._disconnect, 1, 1)
        grid.addWidget(self._pair, 2, 1)
        grid.addWidget(self._remove, 3, 1)
        grid.addWidget(self._trusted, 4, 1)
        grid.addWidget(self._blocked, 5, 1)
        self.setLayout(grid)

    def setEnabled(self, isEnabled):
        self._list.setEnabled(isEnabled)
        item = None
        if isEnabled:
            item = next(iter(self._list.selectedItems()), None)
        self._on_item_changed(item, None)

    def startDiscovery(self):
        self.interface.StartDiscovery()

    def stopDiscovery(self):
        self.interface.StopDiscovery()

    def add_device(self, path, dev):
        item = DeviceItem(
            self._list, type=QtGui.QTreeWidgetItem.Type, path=path, dev=dev)
        item.properties.connect_to_signal(
            'PropertiesChanged', self._get_on_properties_changed(item))

    def remove_device(self, path):
        for i in range(self._list.topLevelItemCount()):
            item = self._list.topLevelItem(i)
            if item and item._path == path:
                self._list.takeTopLevelItem(i)
                item._dev = None

    def _on_item_changed(self, current, previous):
        if current:
            self._connect.setEnabled(not current.getProperty('Connected'))
            self._disconnect.setEnabled(current.getProperty('Connected'))
            self._pair.setEnabled(not current.getProperty('Paired'))
            self._trusted.setChecked(current.getProperty('Trusted'))
            self._blocked.setChecked(current.getProperty('Blocked'))
        else:
            self._connect.setEnabled(False)
            self._disconnect.setEnabled(False)
            self._pair.setEnabled(False)
        self._remove.setEnabled(bool(current))
        self._trusted.setEnabled(bool(current))
        self._blocked.setEnabled(bool(current))

    def _get_on_properties_changed(self, item):
        def _on_properties_changed(iface, data, s):
            if item.isSelected():
                if iface == 'org.bluez.Device1':
                    if 'Connected' in data:
                        self._connect.setEnabled(not data['Connected'])
                        self._disconnect.setEnabled(data['Connected'])
                    if 'Paired' in data:
                        self._pair.setEnabled(not data['Paired'])
                    if 'Trusted' in data:
                        self._trusted.setChecked(data['Trusted'])
                    if 'Blocked' in data:
                        self._blocked.setChecked(data['Blocked'])
        return _on_properties_changed

    def _on_connect(self):
        item = next(iter(self._list.selectedItems()), None)
        if item:
            item.connect()

    def _on_disconnect(self):
        item = next(iter(self._list.selectedItems()), None)
        if item:
            item.disconnect()

    def _on_pair(self):
        item = next(iter(self._list.selectedItems()), None)
        if item:
            self._thread.delay(item.interface, 'Pair')
            # item.pair()

    def _on_remove(self):
        item = next(iter(self._list.selectedItems()), None)
        if item:
            self.interface.RemoveDevice(item._dev)

    def _on_trusted(self):
        item = next(iter(self._list.selectedItems()), None)
        if item:
            item.trusted()

    def _on_blocked(self):
        item = next(iter(self._list.selectedItems()), None)
        if item:
            item.blocked()
