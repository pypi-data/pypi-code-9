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
import sys

if sys.version_info < (3,0,0):
    import Queue
else:
    import queue as Queue

from PyQt4 import QtGui
from PyQt4 import QtCore


# class Canceled(dbus.DBusException):
#     _dbus_error_name = "org.bluez.Error.Canceled"


# class Rejected(dbus.DBusException):
#     _dbus_error_name = "org.bluez.Error.Rejected"


class DeviceThread(QtCore.QThread):
    def __init__(self):
        super(DeviceThread, self).__init__()
        self._queue = Queue.Queue()
        self._running = True

    def __del__(self):
        self.wait()

    def stop_me(self):
        self._running = False

    def run(self):
        while self._running:
            try:
                interface, task_name = self._queue.get()
                task = getattr(interface, task_name)
                task()
                self._queue.task_done()
            except Queue.Empty:
                time.sleep(0.1)

    def delay(self, interface, task_name):
        self._queue.put((interface, task_name))
