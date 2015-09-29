# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ScreamingMercury/SettingsWindow.ui'
#
# Created: Mon Sep 21 15:54:04 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_SettingsWindow(object):
    def setupUi(self, SettingsWindow):
        SettingsWindow.setObjectName("SettingsWindow")
        SettingsWindow.resize(355, 145)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/main/cog.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        SettingsWindow.setWindowIcon(icon)
        self.verticalLayout_2 = QtGui.QVBoxLayout(SettingsWindow)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox = QtGui.QGroupBox(SettingsWindow)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.minifyJsonCheckBox = QtGui.QCheckBox(self.groupBox)
        self.minifyJsonCheckBox.setObjectName("minifyJsonCheckBox")
        self.verticalLayout.addWidget(self.minifyJsonCheckBox)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.groupBox_2 = QtGui.QGroupBox(SettingsWindow)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.comboBox = QtGui.QComboBox(self.groupBox_2)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.verticalLayout_3.addWidget(self.comboBox)
        self.verticalLayout_2.addWidget(self.groupBox_2)

        self.retranslateUi(SettingsWindow)
        QtCore.QMetaObject.connectSlotsByName(SettingsWindow)

    def retranslateUi(self, SettingsWindow):
        SettingsWindow.setWindowTitle(QtGui.QApplication.translate("SettingsWindow", "Настройки", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("SettingsWindow", "Json минификация", None, QtGui.QApplication.UnicodeUTF8))
        self.minifyJsonCheckBox.setText(QtGui.QApplication.translate("SettingsWindow", "Минифицировать json файлы для контейнера", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("SettingsWindow", "Тип отрисоки", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setItemText(0, QtGui.QApplication.translate("SettingsWindow", "Нормальная(Исходные изображения)", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setItemText(1, QtGui.QApplication.translate("SettingsWindow", "Отладочная(Схематичная, прямоугольники изображений)", None, QtGui.QApplication.UnicodeUTF8))

import resources_rc
