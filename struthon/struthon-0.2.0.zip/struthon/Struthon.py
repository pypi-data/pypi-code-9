'''
--------------------------------------------------------------------------
Copyright (C) 2015 Lukasz Laba <lukaszlab@o2.pl>

File version 0.2 date 2015-07-06

This file is part of Struthon.
Struthon is a range of free open source structural engineering design 
Python applications.
http://struthon.org/

Struthon is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

Struthon is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Foobar; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
--------------------------------------------------------------------------
'''

import sys
import os
import time

from PyQt4 import QtCore, QtGui

from mainwindow_ui import Ui_MainWindow

class MAINWINDOW(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton_SCMS.clicked.connect(self.runSCMS)
        self.ui.pushButton_SSSB.clicked.connect(self.runSSSB)
        
    def runSCMS(self):
        os.startfile(os.path.dirname(__file__)+'\ConcreteMonoSection\ConcreteMonoSection.py')
    def runSSSB(self):
        os.startfile(os.path.dirname(__file__)+'\SteelSectionBrowser\SteelSectionBrowser.py')

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = MAINWINDOW()
    myapp.show()
    sys.exit(app.exec_())
