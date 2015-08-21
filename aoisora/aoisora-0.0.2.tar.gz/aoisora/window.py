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

from .device.tree import DeviceTreeWidget


class MainWindow(QtGui.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(QtGui.QMainWindow, self).__init__(*args, **kwargs)

        self._bus = dbus.SystemBus()
        root = self._bus.get_object('org.bluez', '/')
        bluez = self._bus.get_object('org.bluez', '/org/bluez')

        manager = dbus.Interface(root, 'org.freedesktop.DBus.ObjectManager')
        manager.connect_to_signal(
            'InterfacesAdded', self._on_interfaces_added)
        manager.connect_to_signal(
            'InterfacesRemoved', self._on_interfaces_removed)

        objects = manager.GetManagedObjects()
        adapters = dict(filter(
                lambda x: 'org.bluez.Adapter1' in x[1], objects.items()))
        devices = dict(filter(
                lambda x: 'org.bluez.Device1' in x[1], objects.items()))

        hci0 = self._bus.get_object(
            'org.bluez', next(iter(adapters.keys()), None))

        self._devices = DeviceTreeWidget(dev=hci0)
        powered = self._devices.getProperty('Powered') or False
        discoverable = self._devices.getProperty('Discoverable') or False
        discovering = self._devices.getProperty('Discovering') or False

        self._devices.setEnabled(powered)
        for path in devices.keys():
            dev = self._bus.get_object('org.bluez', path)
            self._devices.add_device(path, dev)

        self._devices.properties.connect_to_signal(
            'PropertiesChanged', self._on_properties_changed)

        self.resize(800, 400)
        self.setWindowTitle('AoiSora - Bluetooth Manager')
        self._power = QtGui.QCheckBox('Enabled')
        self._power.setChecked(powered)
        self._power.clicked.connect(self._on_power)

        self._visibility = QtGui.QCheckBox('Visible')
        self._visibility.setChecked(discoverable)
        self._visibility.setEnabled(powered)
        self._visibility.clicked.connect(self._on_visibility)

        text = 'Stop' if self._devices.getProperty('Discovering') else 'Scan'
        self._scan = QtGui.QPushButton(text)
        self._scan.setEnabled(powered)
        self._scan.clicked.connect(self._on_scan)

        toolbar = self.addToolBar('Toolbar')
        # toolbar.addWidget(self._scan)
        toolbar.addWidget(self._visibility)
        spacer = QtGui.QWidget()
        spacer.setSizePolicy(
            QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        toolbar.addWidget(spacer)
        toolbar.addWidget(self._power)

        self.setCentralWidget(self._devices)

        if powered:
            self._devices.startDiscovery()

    def _on_power(self):
        value = self._devices.getProperty('Powered')
        self._devices.setProperty('Powered', not value)

    def _on_visibility(self):
        value = self._devices.getProperty('Discoverable')
        self._devices.setProperty('Discoverable', not value)

    def _on_scan(self):
        if self._devices.getProperty('Discovering'):
            self._devices.stopDiscovery()
        else:
            self._devices.startDiscovery()

    def _on_interfaces_added(self, path, data):
        if 'org.bluez.Device1' in data:
            dev = self._bus.get_object('org.bluez', path)
            self._devices.add_device(path, dev)

    def _on_interfaces_removed(self, path, data):
        if 'org.bluez.Device1' in data:
            self._devices.remove_device(path)

    def _on_properties_changed(self, iface, data, s):
        if iface == 'org.bluez.Adapter1':
            if 'Powered' in data:
                self._power.setChecked(data['Powered'])
                self._visibility.setEnabled(data['Powered'])
                self._scan.setEnabled(data['Powered'])
                self._devices.setEnabled(data['Powered'])
                if data['Powered']:
                    self._devices.startDiscovery()
            if 'Discoverable' in data:
                self._visibility.setChecked(data['Discoverable'])
            if 'Discovering' in data:
                text = 'Stop' if data['Discovering'] else 'Scan'
                self._scan.setText(text)
