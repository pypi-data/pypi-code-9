from PySide.QtGui import *
from PySide.QtCore import *
from karmadbg.uicore.async import async
from karmadbg.uicore.basewidgets import NativeDataViewWidget, AutoMutex

from karmadbg.dbgcore.varprint import getLocals, getLocal, getTypedVar

class VarItem(QStandardItem):

    def __init__(self, uimanager, varName, parentName, varType, varLocation):
        super(VarItem,self).__init__(varName)
        self.uimanager = uimanager
        self.name = varName
        self.fullName = "%s.%s" % (parentName, varName)
        self.type = varType
        self.location = varLocation


class LocalVarsWidget(NativeDataViewWidget):

    def __init__(self, widgetSettings, uimanager):
        super(LocalVarsWidget, self).__init__(uimanager)
        self.uimanager = uimanager

        self.treeModel = QStandardItemModel(0,4)
        self.buildHeader()

        self.treeView = QTreeView()
        self.treeView.setModel(self.treeModel)

        self.treeView.expanded.connect(self.onExpandItem)

        self.setWidget(self.treeView)
        self.setWindowTitle(widgetSettings.title)
        self.uimanager.mainwnd.addDockWidget(Qt.TopDockWidgetArea, self)
        self.updateMutex = QMutex()

    def dataUnavailable(self):
        self.treeModel.clear()
        self.buildHeader()

    def buildHeader(self):
        for section, title in { 0 : "Name", 1 : "Value", 2 : "Type", 3 : "Location"}.items():
            self.treeModel.setHorizontalHeaderItem( section, QStandardItem(title) )

    @async
    def dataUpdate(self):

        yield( self.uimanager.debugClient.lockMutexAsync(self.updateMutex) )

        try:

            self.treeModel.clear()
            self.buildHeader()

            localNames = yield( self.uimanager.debugClient.callServerAsync(getLocals ) )

            for localName in localNames:
                varName, varType, varLocation, shortValue, subitems = yield( self.uimanager.debugClient.callServerAsync(getLocal, localName) )
                treeItem = VarItem(self.uimanager, varName, None, varType, varLocation)
                row = [ treeItem, QStandardItem(shortValue), QStandardItem(varType), QStandardItem(hex(varLocation)) ]

                for fieldName, fieldType, fieldLocation, fieldValue in subitems:
                    fieldItem = VarItem(self.uimanager, fieldName, varName, fieldType, fieldLocation)
                    fieldRow = [ fieldItem, QStandardItem(fieldValue), QStandardItem(fieldType), QStandardItem(hex(fieldLocation)) ]
                    treeItem.appendRow(fieldRow)

                self.treeModel.appendRow(row)

            self.treeView.resizeColumnToContents(0)

        except Exception as ex:
            pass

        self.updateMutex.unlock()

    @async
    def onExpandItem(self, modelIndex):
        expandedItem = self.treeModel.itemFromIndex(modelIndex)
        for r in range(expandedItem.rowCount()):
            childItem = expandedItem.child(r)
            if not childItem.hasChildren():
                varName, varType, varLocation, shortValue, subitems = yield( self.uimanager.debugClient.callServerAsync(getLocal, childItem.fullName) )
                for fieldName, fieldType, fieldLocation, fieldValue in subitems:
                    fieldItem = VarItem(self.uimanager, fieldName, childItem.fullName, fieldType, fieldLocation)
                    fieldRow = [ fieldItem, QStandardItem(fieldValue), QStandardItem(fieldType), QStandardItem(hex(fieldLocation)) ]
                    childItem.appendRow(fieldRow)

        self.treeView.resizeColumnToContents(0)


class WatchWidget(NativeDataViewWidget):
    def __init__(self, widgetSettings, uimanager):
        super(WatchWidget, self).__init__(uimanager)
        self.uimanager = uimanager

        self.treeModel = QStandardItemModel(0,4)
        self.buildHeader()

        self.treeModel.itemChanged.connect(self.onItemChanged)

        self.treeView = QTreeView()
        self.treeView.setModel(self.treeModel)
        self.treeView.expanded.connect(self.onExpandItem)

        self.emptyItem = QStandardItem("")
        self.treeModel.appendRow(self.emptyItem)

        self.setWidget(self.treeView)
        self.setWindowTitle(widgetSettings.title)
        self.uimanager.mainwnd.addDockWidget(Qt.TopDockWidgetArea, self)
        self.updateMutex = QMutex()
        
    def onItemChanged(self,item):
        if item is self.emptyItem:
            self.emptyItem = QStandardItem("")
            self.treeModel.appendRow(self.emptyItem)
            self.dataUpdate()
        elif item.column() == 0 and item.text() == "":
            self.treeModel.removeRow(item.row())

    def dataUnavailable(self):
        pass

    def buildHeader(self):
        for section, title in { 0 : "Name", 1 : "Value", 2 : "Type", 3 : "Location"}.items():
            self.treeModel.setHorizontalHeaderItem( section, QStandardItem(title) )

    @async
    def dataUpdate(self):

        yield( self.uimanager.debugClient.lockMutexAsync(self.updateMutex) )

        try:

            for r in range(self.treeModel.rowCount() - 1):
                treeItem = self.treeModel.item(r)
                varName, varType, varLocation, shortValue, subitems = yield( self.uimanager.debugClient.callServerAsync(getTypedVar, treeItem.text() ) )
                treeItem = VarItem(self.uimanager, varName, None, varType, varLocation)
                self.treeModel.setItem( r, 0, treeItem)
                self.treeModel.setItem( r, 1, QStandardItem(shortValue) )
                self.treeModel.setItem( r, 2, QStandardItem(varType) )
                self.treeModel.setItem( r, 3, QStandardItem(hex(varLocation)) )

                for fieldName, fieldType, fieldLocation, fieldValue in subitems:
                    fieldItem = VarItem(self.uimanager, fieldName, varName, fieldType, fieldLocation)
                    fieldRow = [ fieldItem, QStandardItem(fieldValue), QStandardItem(fieldType), QStandardItem(hex(fieldLocation)) ]
                    treeItem.appendRow(fieldRow)

            self.treeView.resizeColumnToContents(0) 

        except Exception as ex:
            pass

        self.updateMutex.unlock()

    @async
    def onExpandItem(self, modelIndex):
        expandedItem = self.treeModel.itemFromIndex(modelIndex)
        for r in range(expandedItem.rowCount()):
            childItem = expandedItem.child(r)
            if not childItem.hasChildren():
                varName, varType, varLocation, shortValue, subitems = yield( self.uimanager.debugClient.callServerAsync(getTypedVar, childItem.fullName) )
                for fieldName, fieldType, fieldLocation, fieldValue in subitems:
                    fieldItem = VarItem(self.uimanager, fieldName, childItem.fullName, fieldType, fieldLocation)
                    fieldRow = [ fieldItem, QStandardItem(fieldValue), QStandardItem(fieldType), QStandardItem(hex(fieldLocation)) ]
                    childItem.appendRow(fieldRow)

        self.treeView.resizeColumnToContents(0)
 