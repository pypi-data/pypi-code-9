# -*- coding: utf-8 -*-

from PySide import QtGui
from PySide import QtCore

class MessageBox(QtGui.QMessageBox):
    def __init__(self, title, text, label = None, buttons = QtGui.QMessageBox.Ok, default = None, glyph = None, parent = None):
        QtGui.QMessageBox.__init__(self, parent)
        self.setWindowTitle(title)
        self.setText(text)
        self.setStandardButtons(buttons)
        if default:
            self.setDefaultButton(default)
        if glyph:
            self.setIcon(glyph)
        if label:
            self.check = True
            self.checkBox = QtGui.QCheckBox()
            self.checkBox.setText(label)
            self.layout().addWidget(self.checkBox, 1, 1, QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)
        else:
            self.check = False

    def exec_(self, *args, **kwargs):
        accepted = super(MessageBox, self).exec_()
        if self.check:
            return accepted, self.checkBox.isChecked()
        else:
            return accepted
