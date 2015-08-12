# -*- coding: utf-8 -*-

#
# File dialog for open and save operations
#

import os
import getpass

from PySide import QtGui
from PySide import QtCore

from common import CommonDialog

class FileListWidget(QtGui.QListWidget):

    directoryActivated = QtCore.Signal(unicode)
    fileActivated = QtCore.Signal(unicode)
    fileSelected = QtCore.Signal(unicode)
    filesSelected = QtCore.Signal(list)
    upRequested = QtCore.Signal()
    updateRequested = QtCore.Signal()

    def __init__(self, parent):
        self.parent = parent
        super(FileListWidget, self).__init__(parent)
        self.itemSelectionChanged.connect(self.selectItem)
        self.itemDoubleClicked.connect(self.activateItem)

    def setExtendedSelection(self):
        self.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.itemSelectionChanged.disconnect(self.selectItem)
        self.itemSelectionChanged.connect(self.processSelectionChanged)

    def processSelectionChanged(self):
        items = filter(lambda x: x.type() != 0, self.selectedItems())
        names = map(lambda x: x.text(), items)
        self.filesSelected.emit(names)

    def resizeEvent(self, event):
        self.updateRequested.emit()
        super(FileListWidget, self).resizeEvent(event)

    def wheelEvent(self, event):
        sb = self.horizontalScrollBar()
        minValue = sb.minimum()
        maxValue = sb.maximum()
        if sb.isVisible() and maxValue > minValue:
            sb.setValue(sb.value() + (-1 if event.delta() > 0 else 1))
        super(FileListWidget, self).wheelEvent(event)

    def keyPressEvent(self, event):
        modifiers = event.modifiers()
        if event.key() == int(QtCore.Qt.Key_Return) and modifiers == QtCore.Qt.NoModifier:
            if len(self.selectedItems()) > 0:
                item = self.selectedItems()[0]
                if item.type() == 0:  # directory
                    self.directoryActivated.emit(item.text())
                else:  # file
                    self.fileActivated.emit(item.text())
        elif event.key() == int(QtCore.Qt.Key_Backspace) and modifiers == QtCore.Qt.NoModifier:
            self.upRequested.emit()
        elif event.key() == int(QtCore.Qt.Key_F5) and modifiers == QtCore.Qt.NoModifier:
            self.updateRequested.emit()
        else:
            super(FileListWidget, self).keyPressEvent(event)

    def selectItem(self):
        if len(self.selectedItems()) > 0:
            item = self.selectedItems()[0]
            if item.type() == 1:  # file
                self.fileSelected.emit(item.text())

    def activateItem(self):
        if len(self.selectedItems()) > 0:
            item = self.selectedItems()[0]
            if item.type() == 0:  # directory
                self.directoryActivated.emit(item.text())
            else:  # file
                self.fileActivated.emit(item.text())

class Dialog(CommonDialog):

    def __init__(self, parent = None):
        super(Dialog, self).__init__(parent)

        self.pathEdit = QtGui.QLineEdit(self)
        self.pathEdit.setReadOnly(True)
        self.pathEdit.setStyleSheet('QLineEdit { background: rgb(230, 230, 230); selection-background-color: rgb(128, 128, 128); }')
        self.filterBox = QtGui.QComboBox(self)
        self.fileEdit = QtGui.QLineEdit(self)

        self.view = FileListWidget(self)
        self.view.setWrapping(True)
        self.view.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.view.directoryActivated.connect(self.activateDirectoryFromView)
        self.view.fileActivated.connect(self.activateFileFromView)
        self.view.fileSelected.connect(self.selectFileItem)
        self.view.upRequested.connect(self.goUp)
        self.view.updateRequested.connect(self.updateView)

        self.openButton = QtGui.QPushButton('Select', self)
        self.openButton.clicked.connect(self.accept)
        self.cancelButton = QtGui.QPushButton('Cancel', self)
        self.cancelButton.clicked.connect(self.reject)

        size = QtCore.QSize(32, 24)
        self.upButton = QtGui.QPushButton('Up')
        self.upButton.setToolTip('Go up')
        self.upButton.setMinimumSize(size)
        self.upButton.setMaximumSize(size)
        self.upButton.clicked.connect(self.goUp)

        size = QtCore.QSize(56, 24)
        self.refreshButton = QtGui.QPushButton('Reload')
        self.refreshButton.setToolTip('Reload file list')
        self.refreshButton.setMinimumSize(size)
        self.refreshButton.setMaximumSize(size)
        self.refreshButton.clicked.connect(self.updateView)

        self.showHidden = QtGui.QCheckBox('Hidden')
        self.showHidden.setChecked(False)
        self.showHidden.setToolTip('Toggle show hidden files')
        self.showHidden.stateChanged.connect(self.updateView)

        self.places = {}
        self.createLayout()
        self.center()

        self.setFilters([('All Files', ['*.*'])])

        self.setWindowTitle('Select file')
        self.directory = None
        self.setDirectory(os.path.expanduser('~'))

        self.setSizeGripEnabled(True)

    def setShowHidden(self, show):
        self.showHidden.setChecked(show)

    def setFilters(self, filters, selected = 0):
        self.filterBox.clear()
        for name, patterns in filters:
            self.filterBox.addItem('%s (%s)' % (name, ','.join(patterns)), patterns)
        if 0 <= selected < self.filterBox.count():
            self.filterBox.setCurrentIndex(selected)

    def createLayout(self):
        grid = QtGui.QGridLayout()
        subGrid = QtGui.QGridLayout()
        grid.addWidget(QtGui.QLabel('Path:'), 0, 0, QtCore.Qt.AlignRight)

        subGrid.addWidget(self.upButton, 0, 1)
        subGrid.addWidget(self.pathEdit, 0, 2)
        subGrid.addWidget(self.refreshButton, 0, 3)
        subGrid.addWidget(self.showHidden, 0, 4)
        grid.addLayout(subGrid, 0, 1)
        grid.addWidget(self.getPlacesWidget(), 1, 0)
        grid.addWidget(self.view, 1, 1)
        grid.addWidget(QtGui.QLabel('File name:'), 7, 0, QtCore.Qt.AlignRight)
        grid.addWidget(self.fileEdit, 7, 1)
        grid.addWidget(QtGui.QLabel('Filter:'), 8, 0, QtCore.Qt.AlignRight)
        grid.addWidget(self.filterBox, 8, 1)
        hbox = QtGui.QGridLayout()
        hbox.addWidget(self.openButton, 0, 0, QtCore.Qt.AlignRight)
        hbox.addWidget(self.cancelButton, 0, 1, QtCore.Qt.AlignRight)
        grid.addLayout(hbox, 9, 1, QtCore.Qt.AlignRight)
        self.setLayout(grid)
        self.setGeometry(200, 100, 600, 400)

    def getPlacesWidget(self):
        w = QtGui.QGroupBox('')
        w.setParent(self)
        box = QtGui.QVBoxLayout()
        box.setAlignment(QtCore.Qt.AlignTop)
        places = [(getpass.getuser(), os.path.realpath(os.path.expanduser('~')))]
        places += [(q, q) for q in [os.path.realpath(x.absolutePath()) for x in QtCore.QDir().drives()]]
        for label, loc in places:
            icon = QtGui.QFileIconProvider().icon(QtCore.QFileInfo(loc))
            driveBtn = QtGui.QRadioButton(label)
            driveBtn.setIcon(icon)
            driveBtn.setToolTip(loc)
            driveBtn.setProperty('path', loc)
            driveBtn.clicked.connect(self.goToPlace)
            self.places[loc] = driveBtn
            box.addWidget(driveBtn)
        w.setLayout(box)
        return w

    def exec_(self, *args, **kwargs):
        self.updateView()
        self.filterBox.currentIndexChanged.connect(self.updateView)
        accepted = super(Dialog, self).exec_()
        self.filterBox.currentIndexChanged.disconnect(self.updateView)
        return self.getResult() if accepted == 1 else None

    def goToPlace(self):
        sender = self.sender()
        self.setDirectory(sender.property('path'), False)

    def getResult(self):
        tf = self.fileEdit.text()
        sf = self.getFilePath(tf)
        return sf, os.path.dirname(sf), tf.split(os.pathsep)

    def getPatters(self):
        idx = self.filterBox.currentIndex()
        if idx >= 0:
            return self.filterBox.itemData(idx)
        else:
            return []

    def updateView(self):
        self.view.clear()
        qdir = QtCore.QDir(self.directory)
        qdir.setNameFilters(self.getPatters())
        filters = QtCore.QDir.Dirs | QtCore.QDir.AllDirs | QtCore.QDir.Files | QtCore.QDir.NoDot | QtCore.QDir.NoDotDot
        if self.showHidden.isChecked():
            filters = filters | QtCore.QDir.Hidden
        entries = qdir.entryInfoList(
            filters = filters,
            sort = QtCore.QDir.DirsFirst | QtCore.QDir.Name
        )
        fpath = self.getFilePath('..')
        if os.path.exists(fpath) and fpath != self.directory:
            icon = QtGui.QFileIconProvider().icon(QtCore.QFileInfo(self.directory))
            QtGui.QListWidgetItem(icon, '..', self.view, 0)
        for info in entries:
            icon = QtGui.QFileIconProvider().icon(info)
            suf = info.completeSuffix()
            name, tp = (info.fileName(), 0) if info.isDir() else ('%s%s' % (info.baseName(), '.%s' % suf if suf else ''), 1)
            QtGui.QListWidgetItem(icon, name, self.view, tp)
        self.view.setFocus()

    def setDirectory(self, path, checkPlace = True):
        self.directory = os.path.realpath(path)
        self.pathEdit.setText(self.directory)
        self.fileEdit.setText('')
        if checkPlace:
            for loc in self.places:
                rb = self.places[loc]
                rb.setAutoExclusive(False)
                rb.setChecked(loc.lower() == self.directory.lower())
                rb.setAutoExclusive(True)
        self.updateView()
        self.upButton.setEnabled(not self.cantGoUp())

    def goUp(self):
        self.setDirectory(os.path.dirname(self.directory))

    def cantGoUp(self):
        return os.path.dirname(self.directory) == self.directory

    def activateDirectoryFromView(self, name):
        self.setDirectory(os.path.join(self.directory, name))

    def activateFileFromView(self, name):
        self.fileEdit.setText(name)
        self.accept()

    def selectFileItem(self, name):
        self.fileEdit.setText(name)

    def getFilePath(self, fname):
        sname = fname.split(os.pathsep)[0]
        return os.path.realpath(os.path.join(os.path.abspath(self.directory), sname))


class OpenFileDialog(Dialog):

    def __init__(self, parent = None, multi = False):
        super(OpenFileDialog, self).__init__(parent)
        if multi:
            self.view.setExtendedSelection()
            self.view.filesSelected.connect(self.selectFileItems)
        self.openButton.setText('Open')
        self.setWindowTitle('Open file')

    def selectFileItems(self, names):
        self.fileEdit.setText(os.pathsep.join(names))

    def accept(self, *args, **kwargs):
        selectedFile, selectedDir, selectedFileName = self.getResult()
        if not os.path.isdir(selectedFile):
            if os.path.exists(selectedFile):
                super(Dialog, self).accept()
            else:
                messageBox = QtGui.QMessageBox()
                messageBox.setWindowTitle('Confirm file selection')
                messageBox.setText('File "%s" does not exist' % selectedFile)
                messageBox.exec_()


class SaveFileDialog(Dialog):

    def __init__(self, parent = None):
        super(SaveFileDialog, self).__init__(parent)
        self.openButton.setText('Save')
        self.setWindowTitle('Save file')
        size = QtCore.QSize(42, 24)
        self.newDirectoryButton = QtGui.QPushButton('New')
        self.newDirectoryButton.setToolTip('Create new directory')
        self.newDirectoryButton.setMinimumSize(size)
        self.newDirectoryButton.setMaximumSize(size)
        self.newDirectoryButton.clicked.connect(self.createNewDirectory)
        self.layout().itemAtPosition(0, 1).addWidget(self.newDirectoryButton, 0, 5)

    def createNewDirectory(self):
        name, ok = QtGui.QInputDialog.getText(self, 'New directory name', 'Name:', QtGui.QLineEdit.Normal, 'New directory')
        if ok and name:
            path = os.path.join(self.directory, name)
            if os.path.exists(path):
                msgBox = QtGui.QMessageBox(self)
                msgBox.setWindowTitle('Error')
                msgBox.setText('Directory already exists')
                msgBox.exec_()
            else:
                try:
                    os.makedirs(path)
                    self.updateView()
                except os.error, e:
                    msgBox = QtGui.QMessageBox(self)
                    msgBox.setWindowTitle('Error')
                    msgBox.setText('Can not create directory')
                    msgBox.exec_()

    def accept(self, *args, **kwargs):
        selectedFile, selectedDir, selectedFileName = self.getResult()
        if not os.path.isdir(selectedFile):
            if os.path.exists(selectedFile):
                messageBox = QtGui.QMessageBox()
                messageBox.setWindowTitle('Confirm file selection')
                messageBox.setText('File "%s" exists.\nDo you want to overwrite it?' % selectedFile)
                messageBox.setStandardButtons(QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
                messageBox.setDefaultButton(QtGui.QMessageBox.No)
                rv = messageBox.exec_()
                if rv == QtGui.QMessageBox.Yes and not os.path.isdir(selectedFile):
                    super(Dialog, self).accept()
            else:
                super(Dialog, self).accept()


