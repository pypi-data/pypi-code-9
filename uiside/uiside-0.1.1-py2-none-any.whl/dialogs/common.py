# -*- coding: utf-8 -*-

from PySide import QtGui


class CommonDialog(QtGui.QDialog):

    def __init__(self, parent = None):
        super(CommonDialog, self).__init__(parent)

    def center(self):
        frameGeometry = self.frameGeometry()
        frameGeometry.moveCenter(QtGui.QDesktopWidget().availableGeometry().center())
        self.move(frameGeometry.topLeft())
