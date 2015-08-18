#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto
# @Date:   2015-07-06 00:39:05
# @Last Modified by:   Jonathan Prieto 
# @Last Modified time: 2015-07-07 01:46:40

import logging
import os
import sys

from PySide import QtGui, QtCore
from PySide.QtGui import (
    QFileDialog,
    QGridLayout,
    QGroupBox,
    QCheckBox,
    QTextBrowser,
    QPushButton,
    QMessageBox,
    QSpinBox
)
from atxt.utils import remove
from constants import (
    BTN_BROWSER,
    BTN_SAVE_LOG,
    LABEL_BOX_SAVE_IN,
    LABEL_BOX_URL,
    LABEL_BOX_LAYOUT1,
    LABEL_BOX_LAYOUT2,
    LABEL_DEPTH,
    LABEL_OVERWRITE,
    MSG_SAVE_IN,
    NAME_FOLDER_TXT,
    TITLE_WINDOW,
    TOOLTIP_BOX_SAVEIN,
    TOOLTIP_DEPTH,
    TOOLTIP_OVERWRITE,
    TOOLTIP_SAVEIN,
    TOOLTIP_SCAN,
    WARNING_LONG_PROCESS
)
from digs.logger import Logger
from start import Start



log = Logger.log

path_home = os.path.expanduser('~')
checked = QtCore.Qt.Checked
unchecked = QtCore.Qt.Unchecked


class QtHandler(logging.Handler):

    def __init__(self):
        logging.Handler.__init__(self)

    def emit(self, record):
        record = self.format(record)
        if record:
            XStream.stdout().write('%s\n' % record)

handler = QtHandler()
handler.setLevel(logging.INFO)
log.addHandler(handler)


class XStream(QtCore.QObject):

    """ http://stackoverflow.com/questions/24469662/
    how-to-redirect-logger-output-into-pyqt-text-widget"""

    _stdout = None
    _stderr = None
    messageWritten = QtCore.Signal(str)

    def flush(self):
        pass

    def fileno(self):
        return -1

    def write(self, msg):
        if (not self.signalsBlocked()):
            self.messageWritten.emit(msg)

    @staticmethod
    def stdout():
        if (not XStream._stdout):
            XStream._stdout = XStream()
            sys.stdout = XStream._stdout
        return XStream._stdout

    @staticmethod
    def stderr():
        if (not XStream._stderr):
            XStream._stderr = XStream()
            sys.stderr = XStream._stderr
        return XStream._stderr


class Window(QtGui.QWidget):
    layout = QGridLayout()
    _layout1 = QtGui.QVBoxLayout()
    _layout2 = QtGui.QVBoxLayout()

    def __init__(self):
        QtGui.QWidget.__init__(self)
        log.debug('GUI digs')
        self.setWindowTitle(TITLE_WINDOW)
        self.setFixedSize(850, 400)
        self.setContentsMargins(15, 15, 15, 15)
        self._set_layout_source()
        self._set_layout_save()
        self._set_layout_console()
        self._set_layout2()

        self._connect_acctions()
        box = QGroupBox(LABEL_BOX_LAYOUT1)
        box.setLayout(self._layout1)
        self.layout.addWidget(box, 0, 0)

        box = QGroupBox(LABEL_BOX_LAYOUT2)
        box.setLayout(self._layout2)
        self.layout.addWidget(box, 0, 1)
        self.setLayout(self.layout)

        XStream.stdout().messageWritten.connect(self._cursor_visible)
        XStream.stderr().messageWritten.connect(self._cursor_visible)

    def _cursor_visible(self, value):
        self._console.insertPlainText(value)
        self._console.ensureCursorVisible()

    def _set_layout_source(self):

        self._layout1 = QtGui.QVBoxLayout()
        self._layout1.addStretch(1)

        self._edt_url = QtGui.QLineEdit()
        self._edt_url.setFixedSize(400, 20)
        self._edt_url.setAlignment(QtCore.Qt.AlignRight)

        box = QGroupBox(LABEL_BOX_URL)
        ly = QGridLayout()
        ly.addWidget(self._edt_url, 0, 1)
        box.setLayout(ly)
        self._layout1.addWidget(box)

    def _set_layout_save(self):
        self._label_save = QtGui.QLabel(MSG_SAVE_IN)
        self._edt_save = QtGui.QLineEdit("")
        self._edt_save.setFixedSize(350, 20)
        self._edt_save.setToolTip(TOOLTIP_SAVEIN)
        self._edt_save.setAlignment(QtCore.Qt.AlignRight)

        self._btn2 = QtGui.QPushButton(BTN_BROWSER)
        self._btn2.clicked.connect(self.set_directory_save_in)

        box = QGroupBox(LABEL_BOX_SAVE_IN)
        box.setToolTip(TOOLTIP_BOX_SAVEIN)
        ly = QGridLayout()
        ly.addWidget(self._btn2, 0, 0)
        ly.addWidget(self._edt_save, 0, 1)
        box.setLayout(ly)
        self._layout1.addWidget(box)

    def _set_layout_console(self):
        self._console = QTextBrowser(self)
        frameStyle = QtGui.QFrame.Sunken | QtGui.QFrame.Panel
        self._console.setFrameStyle(frameStyle)
        self._layout1.addWidget(self._console)

    def _save_log(self):
        save_log_dir = QFileDialog.getSaveFileName(
            self, "Save Log File", "", "Text File (*.txt)")
        try:
            remove(save_log_dir[0])
        except Exception, e:
            log.error(e)
        f = QtCore.QFile(save_log_dir[0])
        try:
            if f.open(QtCore.QIODevice.ReadWrite):
                stream = QtCore.QTextStream(f)
                text = self._console.toPlainText()
                text = text.replace('\n', os.linesep)
                exec "stream << text"
                f.flush()
                f.close()

        except Exception, e:
            log.critical(e)

    def _set_layout2(self):

        self._depth = QSpinBox()
        self._depth.setToolTip(TOOLTIP_DEPTH)
        self._depth.setMinimum(0)
        self._depth.setMaximum(100)
        self._depth.setFixedSize(50, 25)

        self._label1 = QtGui.QLabel()
        self._label1.setText(LABEL_DEPTH)

        self._check_overwrite = QCheckBox(LABEL_OVERWRITE)
        self._check_overwrite.setToolTip(TOOLTIP_OVERWRITE)
        self._check_overwrite.setCheckState(checked)

        self._check_sameroot = QCheckBox('Same root for all links')
        self._check_sameroot.setCheckState(checked)

        box = QGroupBox('Options')
        ly = QGridLayout()
        ly.addWidget(self._label1, 0, 0)
        ly.addWidget(self._depth, 0, 1)
        ly.addWidget(self._check_overwrite, 1, 0)
        ly.addWidget(self._check_sameroot, 2, 0)
        box.setLayout(ly)
        self._layout2.addWidget(box)

        self._btn_start = QPushButton("Start")
        self._btn_start.setEnabled(True)

        self._btn_save_log = QtGui.QPushButton(BTN_SAVE_LOG)
        self._btn_save_log.clicked.connect(self._save_log)

        box = QGroupBox('')
        ly = QGridLayout()
        ly.setColumnStretch(1, 1)
        ly.addWidget(self._btn_start,  0, 0)
        ly.addWidget(self._btn_save_log,  1, 0)

        box.setLayout(ly)
        self._layout2.addWidget(box)

    def closeEvent(self, event):
        log.debug("Exit")
        event.accept()

    def on_show_info(self, value):
        QtGui.QMessageBox.information(self, "Information", value)

    def set_directory_save_in(self):
        options_ = QFileDialog.DontResolveSymlinks | QFileDialog.ShowDirsOnly
        directory = QFileDialog.getExistingDirectory(self,
                                                     MSG_SAVE_IN,
                                                     self._edt_save.text(), options_)
        if directory:
            self._edt_save.setText(directory)
            log.debug('--to: %s' % directory)

    def options(self):
        url = self._edt_url.text()

        to = self._edt_save.text()

        opts = {
            '<url>': url,
            '--to': to,
            '-o': self._check_overwrite.isChecked(),
            '--sameroot': self._check_sameroot.isChecked(),
            '--depth': int(self._depth.text()),
        }
        return opts

    def _connect_acctions(self):
        self._btn_start.clicked.connect(self._start)

    def _start(self):
        flags = QMessageBox.StandardButton.Yes
        flags |= QMessageBox.StandardButton.No
        question = WARNING_LONG_PROCESS
        response = QMessageBox.question(self, "Question", question, flags)
        if response == QMessageBox.Yes:
            log.debug("Starting process")
        elif QMessageBox.No:
            log.debug("Starting cancelled")
            return

        self._btn_start.setEnabled(False)
        self._thread = Start(self)
        self._thread.start()
        self._thread.finished.connect(self._thread_finished)
        self._thread.terminated.connect(self._thread_finished)

    def _thread_finished(self):
        self._btn_start.setEnabled(True)
