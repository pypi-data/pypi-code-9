# encoding: utf8
from PySide.QtCore import Qt
from PySide.QtGui import QWidget

from SettingsWindow import Ui_SettingsWindow


class Settings(QWidget, Ui_SettingsWindow):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setupUi(self)

    def keyPressEvent(self, *args, **kwargs):
        if args[0].key() == Qt.Key_Escape:
            self.hide()
