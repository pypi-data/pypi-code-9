import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from GUI import MainWindow


def launch():
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    QTimer.singleShot(0,  lambda: mw.start())
    app.exec_()

launch()
