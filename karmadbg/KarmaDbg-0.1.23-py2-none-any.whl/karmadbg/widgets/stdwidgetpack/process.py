
from PySide.QtGui import QTreeView, QStandardItemModel, QStandardItem
from PySide.QtCore import Qt, QMutex

from karmadbg.uicore.basewidgets import *
from karmadbg.uicore.async import *
from karmadbg.uicore.dbgclient import DebugAsyncCall

from karmadbg.scripts.proclist import * 


class ThreadItem(QStandardItem):

    def __init__(self, threadInfo, uimanager):
        super(ThreadItem,self).__init__("Tid: %x" % threadInfo.tid)
        self.id = threadInfo.id
        self.processId = threadInfo.processId
        self.targetId = threadInfo.targetId
        self.uimanager = uimanager
        self.setEditable(False)

    @async
    def update(self, threadInfo):
        font = self.font()
        font.setBold(threadInfo.isCurrent)
        self.setFont(font)
        raise StopIteration

class ThreadRootItem(QStandardItem):

    def __init__(self, uimanager):
        super(ThreadRootItem,self).__init__("Threads: 0")
        self.uimanager = uimanager
        self.setEditable(False)

    @async
    def update(self, threadsList):

        for i in xrange(len(threadsList)):
            threadItem = self.child(i)
            if not threadItem or threadsList[i].id != threadItem.id:
                threadItem = ThreadItem(threadsList[i], self.uimanager)
                self.insertRow(i, threadItem)
            yield( self.uimanager.debugClient.callFunctionAsync(threadItem.update, threadsList[i]) )

            if len(threadsList) < self.rowCount():
                 self.removeRows( len(threadsList), self.rowCount() - len(threadsList) )

        self.setText("Threads: %d" % len(threadsList))

        raise StopIteration


class ProcessItem(QStandardItem):
    def __init__(self, processInfo, uimanager):
        super(ProcessItem,self).__init__("Pid: %x (%s)" % (processInfo.pid, processInfo.exeName) )
        self.id = processInfo.id
        self.uimanager = uimanager
        self.threadRoot = None
        self.setEditable(False)

    @async
    def update(self, processInfo):
        if not self.threadRoot:
            self.threadRoot = ThreadRootItem(self.uimanager)
            self.appendRow(self.threadRoot)

        yield ( self.uimanager.debugClient.callFunctionAsync(self.threadRoot.update, processInfo.threads) )

        font = self.font()
        font.setBold(processInfo.isCurrent)
        self.setFont(font)

class ProcessRootItem(QStandardItem):

    def __init__(self, uimanager):
        super(ProcessRootItem,self).__init__("Processes: 0")
        self.uimanager = uimanager
        self.setEditable(False)

    @async
    def update(self, processesList):

        for i in xrange(len(processesList)):
            processItem = self.child(i)
            if not processItem or processesList[i].id != processItem.id:
                processItem = ProcessItem(processesList[i], self.uimanager)
                self.insertRow(i, processItem)
            yield( self.uimanager.debugClient.callFunctionAsync(processItem.update, processesList[i]) )

            if len(processesList) < self.rowCount():
                 self.removeRows( len(processesList), self.rowCount() - len(processesList) )

        self.setText("Processes: %d" % len(processesList))

        raise StopIteration

class TargetItem(QStandardItem):

    def __init__(self, targetInfo, uimanager):
        super(TargetItem,self).__init__(targetInfo.desc)
        self.desc = targetInfo.desc
        self.id = targetInfo.id
        self.processRoot = None
        self.uimanager = uimanager
        self.setEditable(False)

    @async
    def update(self,targetInfo):
        if hasattr(targetInfo, "processes"):
            if not self.processRoot:
                self.processRoot = ProcessRootItem(self.uimanager)
                self.appendRow(self.processRoot)

            yield ( self.uimanager.debugClient.callFunctionAsync(self.processRoot.update, targetInfo.processes) )

        font = self.font()
        font.setBold(targetInfo.isCurrent)
        self.setFont(font)

class ProcessExplorerWidget(NativeDataViewWidget):

    def __init__(self, widgetSettings, uimanager):
        super(ProcessExplorerWidget,self).__init__(uimanager)
        self.uimanager = uimanager

        self.treeView = QTreeView()
        self.treeView.setHeaderHidden(True)

        self.treeModel = QStandardItemModel(0,1)

        self.treeView.setSelectionMode(QTreeView.NoSelection)
        self.treeView.setAllColumnsShowFocus(False)
        self.treeView.doubleClicked.connect(self.onItemDblClick)

        self.setWidget(self.treeView)

        self.uimanager.mainwnd.addDockWidget(Qt.TopDockWidgetArea, self)
        self.updateMutex = UpdateMutex()

    def dataUnavailable(self):
        self.treeModel.clear()
       
    @async
    def dataUpdate(self):

        yield( self.uimanager.debugClient.lockMutexAsync(self.updateMutex) )

        with AutoQMutex(self.updateMutex) as updateLocker:

            targetsList = yield( self.uimanager.debugClient.callServerAsync(getTargetsList) )

            for i in xrange(len(targetsList)):
                targetItem = self.treeModel.item(i)
                if not targetItem or targetsList[i].id != targetItem.id:
                    targetItem = TargetItem(targetsList[i], self.uimanager)
                    self.treeModel.insertRow(i, targetItem)
                yield( self.uimanager.debugClient.callFunctionAsync(targetItem.update, targetsList[i]) )

            if len(targetsList) < self.treeModel.rowCount():
                 self.treeModel.removeRows( len(targetsList), self.treeModel.rowCount() - len(targetsList) )
            
            self.treeView.setModel(self.treeModel)

    def onItemDblClick(self, modelIndex):
        item = self.treeModel.itemFromIndex(modelIndex)
        if type(item) is ThreadItem:
            self.uimanager.debugClient.callFunction(setCurrentThread, item.targetId, item.processId, item.id )



#class ProcessExplorerWidget(NativeDataViewWidget):

#    def __init__(self, widgetSettings, uimanager):
#        super(ProcessExplorerWidget,self).__init__(uimanager)
#        self.uimanager = uimanager
#        self.uimanager.mainwnd.addDockWidget(Qt.TopDockWidgetArea, self)



































#class BreakpointItem(QStandardItem):

#    def __init__(self, bpOffset):
#        super(BreakpointItem, self).__init__("%x" % bpOffset)
#        self.bpOffset = bpOffset

#class BreakpointRootItem(QStandardItem):
#    def __init__(self, pid):
#        super(BreakpointRootItem,self).__init__("Breakpoints: 0")
#        self.pid = pid
#        self.setEditable(False)

#    def update(self, bpList):
#        self.setRowCount(0)
#        for bp in bpList:
#            bpItem = BreakpointItem(bp)
#            self.appendRow(bpItem)

#        self.setText("Breakpoints: %d" % len(bpList))
#        self.sortChildren(0)

#class ThreadItem(QStandardItem):
#    def __init__(self, pid, tid):
#        super(ThreadItem,self).__init__("Id: %x" % tid)
#        self.pid = pid
#        self.tid = tid
#        self.setEditable(False) 
#        self.setSelectable(False)

#    def update(self, isCurrent):
#        font = self.font()
#        font.setBold(isCurrent)
#        self.setFont(font)

#class ThreadRootItem(QStandardItem):
#    def __init__(self, pid):
#        super(ThreadRootItem,self).__init__("Threads: 0")
#        self.pid = pid
#        self.setEditable(False)

#    def update(self, threadlst, currentThread):

#        #delete stopped threads
#        row = 0
#        while row < self.rowCount():
#            threadItem = self.child(row)
#            for tid in threadlst:
#                if tid == threadItem.tid:
#                    row += 1
#                    continue
#            else:
#                self.removeRow(row)

#        #added new threads
#        for tid, in threadlst:

#            row = 0
#            while row < self.rowCount():
#                threadItem = self.child(row)
#                if threadItem.tid == tid:
#                    break
#                row += 1
#            else:
#                threadItem = ThreadItem(self.pid, tid)
#                self.appendRow(threadItem)

#            threadItem.update(currentThread == tid)

#        self.setText("Threads: %d" % len(threadlst))
#        self.sortChildren(0)


#class ProcessItem(QStandardItem):
#    def __init__(self, pid, exe):
#        super(ProcessItem,self).__init__("Pid: %x (%s)" % (pid, exe) )
#        self.pid = pid
#        self.exe = exe
#        self.setEditable(False)
#        self.processNameItem = QStandardItem( "Name: %s" % exe )
#        self.processNameItem.setEditable(False)
#        self.appendRow(self.processNameItem)
#        self.threadsItem = ThreadRootItem(pid)
#        self.appendRow(self.threadsItem)
#        self.breakpointsItem = BreakpointRootItem(pid)
#        self.appendRow(self.breakpointsItem)

#    def updateThreads(self, threadlst, currentThread):
#        self.threadsItem.update(threadlst, currentThread)

#    def updateBreakpoints(self, breakpointLst):
#        self.breakpointsItem.update(breakpointLst)

#class ProcessExplorerWidget(NativeDataViewWidget):

#    def __init__(self, widgetSettings, uimanager):
#        super(ProcessExplorerWidget,self).__init__(uimanager)
#        self.uimanager = uimanager

#        self.treeView = QTreeView()
#        self.treeView.setHeaderHidden(True)

#        self.treeModel = QStandardItemModel(0,1)

#        self.treeView.setSelectionMode(QTreeView.NoSelection)
#        self.treeView.setAllColumnsShowFocus(False)
#        self.treeView.doubleClicked.connect(self.onItemDblClick)

#        self.setWidget(self.treeView)

#        self.uimanager.mainwnd.addDockWidget(Qt.TopDockWidgetArea, self)

#    def dataUnavailable(self):
#        self.treeModel.clear()

       
#    @async
#    def dataUpdate(self):
#        processesSnapshot = yield(self.uimanager.debugClient.callServerAsync(getProcessThreadList) )

#        for processInfo in processesSnapshot.processList:

#            row = 0
#            while row < self.treeModel.rowCount():
#                processItem = self.treeModel.item(row)
#                if processItem.pid == processInfo.pid:
#                    break
#                row += 1
#            else:
#                processItem = ProcessItem(processInfo.pid, processInfo.exeName)
#                self.treeModel.appendRow(processItem)

#            processItem.updateThreads(processInfo.threadList, processesSnapshot.currentThreadID if processesSnapshot.currentProcessID == processInfo.pid else None )
#            processItem.updateBreakpoints(processInfo.breakpointList)

#        self.treeView.setModel(self.treeModel)

#    def onItemDblClick(self, modelIndex):
#        item = self.treeModel.itemFromIndex(modelIndex)
#        if type(item) is ThreadItem:
#            self.uimanager.debugClient.callFunction(setCurrentThread, item.pid, item.tid)


