# encoding: utf8
from PySide.QtGui import QWidget

from ProgressWindow import (Ui_ProgressWindow)


class Progress(QWidget, Ui_ProgressWindow):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setupUi(self)
