#!/usr/local/lcls/package/python/current/bin/python -d
# encoding: utf-8

'''
Name: logbookForm.py
Author: Shawn Alverson
Created: 2/01/2013

Purpose: Logbook entry form for use with canvas.py
'''

from PyQt4.QtCore import *
from PyQt4.QtGui import *
__all__ = ['logbookForm', 'sendToLogbook']


class logbookForm(QDialog):
    """Dialog GUI for creating logbook entries for both MCC and Physics(DESY) type logbooks"""
    
    def __init__(self, parent=None, image=None, logType='MCC', log='LCLS', deleteOnClose=True):
        from .ui_logbookForm import Ui_logbookForm  # imports Qt gui design file
        
        QDialog.__init__(self, parent)
        if deleteOnClose:
            # If set, object is deleted when close signal is sent
            self.setAttribute(Qt.WA_DeleteOnClose, deleteOnClose)

        self.logui = Ui_logbookForm()
        self.logui.setupUi(self)

        # Initialize variables
        self.mcc_programs = []
        self.physics_programs = []
        self.logMenus = []
        self.logMenuCount = 0
        self.imageType = "png"
        
        # QDir.setCurrent('/u/ad/alverson/cvswork/tools/python/toolbox')
        file = open(self.resourcePath('StyleSheets/LightTheme/lightTheme.qss'), 'r')
        stylesheet = file.read()
        stylesheet.replace('%%', self.resourcePath('StyleSheets/LightTheme/'))
        self.setStyleSheet(stylesheet)
        
        # Check is image is provided and of valid type
        self.image = image
        self.checkImage(image)

        # Set up Logbook pulldowns
        self.logTypeList = ["MCC", "Physics"]
        self.getLogbooks()
        self._connectSlots()
        mccDef = "MCC"
        physDef = "LCLS"
        if logType == "MCC":
            mccDef = log
        else:
            physDef = log
        self.addLogbook(physDef, mccDef, initialInstance=True)

        # Select default log in pulldown
        self.logMenus[0].logType.setCurrentIndex(self.logMenus[0].logType.findText(logType))

    def resourcePath(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        from os import path
        import sys
        
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = path.dirname(path.abspath(__file__))
        return path.join(base_path, relative_path)
    
    def _connectSlots(self):
        QObject.connect(self.logui.submitButton, SIGNAL("clicked()"), self.submitEntry)
        QObject.connect(self.logui.cancelButton, SIGNAL("clicked()"), self.reject)
        QObject.connect(self.logui.resetButton, SIGNAL("clicked()"), self.clearForm)

    def checkImage(self, image):
        if type(image) != QPixmap:
            if image is None:
                image = QPixmap()
            elif type(image) == str or type(image) == str:
                from os import path
                if path.exists(image):
                    if path.splitext(image)[1] == ".gif":
                        self.imageType = "gif"
                    image = QPixmap(image)
                else:
                    raise Exception("Invalid path to image file specified: " + image)
            else:
                raise Exception("Invalid image type: " + str(type(image)) + "! Must provide QPixmap or path to valid image file.")
        self.imagePixmap = image
        self.pinImage()

    def pinImage(self):
        # Scale image file down to 40x40 icon and paint in thumbnail
        if not self.imagePixmap.isNull():
            icon = self.imagePixmap.scaled(50, 50, Qt.KeepAspectRatio, Qt.FastTransformation)
            self.logui.imageFrame.setPixmap(icon)
        else:
            self.logui.imageFrame.setVisible(False)
    
    def getLogbooks(self):
        from urllib.request import urlopen, URLError, HTTPError
        import json
        
        # Retrieve MCC sublogs,
        while True:
            networkFault = False
            log_url = "https://mccelog.slac.stanford.edu/elog/dev/mgibbs/dev_json_logbook_list.php"
            try:
                data = urlopen(log_url, None, 5).read()
                data = json.loads(data.decode('utf8'))
                break
            except URLError as error:
                print("URLError: " + str(error.reason))
                networkFault = True
            except HTTPError as error:
                print("HTTPError: " + str(error.reason))
                networkFault = True
            
            # Ask to repeat if network connection fails
            if networkFault:
                data = [{"name": "MCC"}, {"name": "SPEAR"}, {"name": "NLCTA"}]
                msgBox = QMessageBox()
                msgBox.setText("Cannot connect to MCC Log Server!")
                msgBox.setInformativeText("Load default logbooks?")
                msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Retry)
                msgBox.setDefaultButton(QMessageBox.Retry)
                if msgBox.exec_() != QMessageBox.Retry:
                    break
        
        self.mcc_programs = []
        for i in data:
            self.mcc_programs.append(str(i["name"]))
        self.mcc_programs.sort()
        
        # Set up Physics logbooks
        self.physics_programs = ["LCLS", "FACET"]
    
    def addLogbook(self, physDef= "LCLS", mccDef="MCC", initialInstance=False):
        '''Add new block of logbook selection windows. Only 5 allowed.'''
        if self.logMenuCount < 5:
            self.logMenus.append(LogSelectMenu(self.logui.multiLogLayout, initialInstance))
            self.logMenus[-1].addLogbooks(self.logTypeList[1], self.physics_programs, physDef)
            self.logMenus[-1].addLogbooks(self.logTypeList[0], self.mcc_programs, mccDef)
            self.logMenus[-1].show()
            self.logMenuCount += 1
            if initialInstance:
                # Initial logbook menu can add additional menus, all others can only remove themselves.
                QObject.connect(self.logMenus[-1].logButton, SIGNAL("clicked()"), self.addLogbook)
            else:
                from functools import partial
                QObject.connect(self.logMenus[-1].logButton, SIGNAL("clicked()"), partial(self.removeLogbook, self.logMenus[-1]))
    
    def removeLogbook(self, menu=None):
        '''Remove logbook menu set.'''
        if self.logMenuCount > 1 and menu is not None:
            menu.removeMenu()
            self.logMenus.remove(menu)
            self.logMenuCount -= 1
    
    def selectedLogs(self):
        '''Return selected log books by type.'''
        mcclogs = []
        physlogs = []
        for i in range(len(self.logMenus)):
            logType = self.logMenus[i].selectedType()
            log = self.logMenus[i].selectedProgram()
            if logType == "MCC":
                if log not in mcclogs:
                    mcclogs.append(log)
            elif logType == "Physics":
                if log not in physlogs:
                    physlogs.append(log)
        return mcclogs, physlogs
    
    def acceptedUser(self, logType):
        '''Verify enetered user name is on accepted MCC logbook list.'''
        from urllib2 import urlopen, URLError, HTTPError
        import json
        
        isApproved = False
        
        userName = str(self.logui.userName.text())
        if userName == "":
            return False  # Must have a user name to submit entry
        
        if logType == "MCC":
            networkFault = False
            data = []
            log_url = "https://mccelog.slac.stanford.edu/elog/dev/mgibbs/dev_json_user_list.php/?username=" + userName
            try:
                data = urlopen(log_url, None, 5).read()
                data = json.loads(data)
            except URLError as error:
                print("URLError: " + str(error.reason))
                networkFault = True
            except HTTPError as error:
                print("HTTPError: " + str(error.reason))
                networkFault = True
            
            # If network fails, ask user to verify
            if networkFault:
                msgBox = QMessageBox()
                msgBox.setText("Cannot connect to MCC Log Server!")
                msgBox.setInformativeText("Use entered User name anyway?")
                msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                msgBox.setDefaultButton(QMessageBox.Ok)
                if msgBox.exec_() == QMessageBox.Ok:
                    isApproved = True
            
            if data != [] and (data is not None):
                isApproved = True
        else:
            isApproved = True
        return isApproved
    
    def xmlSetup(self, logType, logList):
        """Create xml file with fields from logbook form."""
        
        from xml.etree.ElementTree import Element, SubElement, ElementTree
        from datetime import datetime
        
        curr_time = datetime.now()
        if logType == "MCC":
            # Set up xml tags
            log_entry = Element('log_entry')
            title     = SubElement(log_entry, 'title')
            program   = SubElement(log_entry, 'program')
            timestamp = SubElement(log_entry, 'timestamp')
            priority  = SubElement(log_entry, 'priority')
            os_user   = SubElement(log_entry, 'os_user')
            hostname  = SubElement(log_entry, 'hostname')
            text      = SubElement(log_entry, 'text')
            log_user  = SubElement(log_entry, 'log_user')

            # Check for multiple logbooks and parse into seperate tags
            logbook = []
            for i in range(len(logList)):
                logbook.append(SubElement(log_entry, 'logbook'))
                logbook[i].text = logList[i].lower()
                           
            # Take care of dummy, unchanging tags first
            log_entry.attrib['type'] = "LOGENTRY"
            program.text = "152"
            priority.text = "NORMAL"
            os_user.text = "nobody"
            hostname.text = "mccelog"
            text.attrib['type'] = "text/plain"
            
            # Handle attachment if image exists
            if not self.imagePixmap.isNull():
                attachment = SubElement(log_entry, 'attachment')
                attachment.attrib['name'] = "Figure 1"
                attachment.attrib['type'] = "image/" + self.imageType
                attachment.text = curr_time.strftime("%Y%m%d_%H%M%S_") + str(curr_time.microsecond) + "." + self.imageType
            
            # Set timestamp format
            timestamp.text = curr_time.strftime("%Y/%m/%d %H:%M:%S")
            
            fileName = "/tmp/" + curr_time.strftime("%Y%m%d_%H%M%S_") + str(curr_time.microsecond) + ".xml"
            
        else:  # If using Physics logbook
            timeString = curr_time.strftime("%Y-%m-%dT%H:%M:%S")
            
            # Set up xml tags
            log_entry = Element(None)
            severity  = SubElement(log_entry, 'severity')
            location  = SubElement(log_entry, 'location')
            keywords  = SubElement(log_entry, 'keywords')
            time      = SubElement(log_entry, 'time')
            isodate   = SubElement(log_entry, 'isodate')
            log_user  = SubElement(log_entry, 'author')
            category  = SubElement(log_entry, 'category')
            title     = SubElement(log_entry, 'title')
            metainfo  = SubElement(log_entry, 'metainfo')
            
            # Handle attachment if image exists
            if not self.imagePixmap.isNull():
                imageFile = SubElement(log_entry, 'link')
                imageFile.text = timeString + "-00." + self.imageType
                thumbnail = SubElement(log_entry, 'file')
                thumbnail.text = timeString + "-00.png"
                
            text      = SubElement(log_entry, 'text')  # Logbook expects Text tag to come last (for some strange reason)
            
            # Take care of dummy, unchanging tags first
            log_entry.attrib['type'] = "LOGENTRY"
            category.text = "USERLOG"
            location.text = "not set"
            severity.text = "NONE"
            keywords.text = "none"
            
            time.text = curr_time.strftime("%H:%M:%S")
            isodate.text = curr_time.strftime("%Y-%m-%d")
            
            metainfo.text = timeString + "-00.xml"
            fileName = "/tmp/" + metainfo.text
            
        # Fill in user inputs
        log_user.text = str(self.logui.userName.text())

        title.text = str(self.logui.titleEntry.text())
        if title.text == "":
            QMessageBox().warning(self, "No Title entered", "Please enter a title for the entry...")
            return None
            
        text.text = str(self.logui.textEntry.toPlainText())
        # If text field is truly empty, ElementTree leaves off tag entirely which causes logbook parser to fail
        if text.text == "":
            text.text = " "
        
        # Create xml file
        xmlFile = open(fileName, "w")
        if logType == "MCC":
            ElementTree(log_entry).write(xmlFile)
        else:
            xmlString = self.prettify(log_entry)
            xmlFile.write(xmlString)
        xmlFile.write("\n")  # Close with newline so cron job parses correctly
        xmlFile.close()
            
        return fileName.rstrip(".xml")

    def prettify(self, elem):
        """Parse xml elements for pretty printing"""
        
        from xml.etree import ElementTree
        from re import sub
        
        rawString = ElementTree.tostring(elem, 'utf-8')
        parsedString = sub(r'(?=<[^/].*>)', '\n', rawString)  # Adds newline after each closing tag
        
        return parsedString[1:]
    
    def prepareImages(self, fileName, logType):
        """Convert supplied QPixmap object to image file."""
        import subprocess
        
        if self.imageType == "png":
            self.imagePixmap.save(fileName + ".png", "PNG", -1)
            if logType == "Physics":
                makePostScript = "convert " + fileName + ".png " + fileName + ".ps"
                process = subprocess.Popen(makePostScript, shell=True)
                process.wait()
                thumbnailPixmap = self.imagePixmap.scaled(500, 450, Qt.KeepAspectRatio)
                thumbnailPixmap.save(fileName + ".png", "PNG", -1)
        else:
            renameImage = "cp " + self.image + " " + fileName + ".gif"
            process = subprocess.Popen(renameImage, shell=True)
            process.wait()
            if logType == "Physics":
                thumbnailPixmap = self.imagePixmap.scaled(500, 450, Qt.KeepAspectRatio)
                thumbnailPixmap.save(fileName + ".png", "PNG", -1)
    
    def submitEntry(self):
        """Process user inputs and subit logbook entry when user clicks Submit button"""
        
        # logType = self.logui.logType.currentText()
        mcclogs, physlogs = self.selectedLogs()
        success = True
        
        if mcclogs != []:
            if not self.acceptedUser("MCC"):
                QMessageBox().warning(self, "Invalid User", "Please enter a valid user name!")
                return
            
            fileName = self.xmlSetup("MCC", mcclogs)
            if fileName is None:
                return
            
            if not self.imagePixmap.isNull():
                self.prepareImages(fileName, "MCC")
            success = self.sendToLogbook(fileName, "MCC")
        
        if physlogs != []:
            for i in range(len(physlogs)):
                fileName = self.xmlSetup("Physics", physlogs[i])
                if fileName is None:
                    return
            
                if not self.imagePixmap.isNull():
                    self.prepareImages(fileName, "Physics")
                success_phys = self.sendToLogbook(fileName, "Physics", physlogs[i])
                success = success and success_phys
            
        self.done(success)
    
    def sendToLogbook(self, fileName, logType, location=None):
        '''Process log information and push to selected logbooks.'''
        import subprocess
        
        success = True
        if logType == "MCC":
            fileString = ""
            if not self.imagePixmap.isNull():
                fileString = fileName + "." + self.imageType
        
            logcmd = "xml2elog " + fileName + ".xml " + fileString
            process = subprocess.Popen(logcmd, shell=True)
            process.wait()
            if process.returncode != 0:
                success = False
        else:
            from shutil import copy

            path = "/u1/" + location.lower() + "/physics/logbook/data/"  # Prod path
            # path = "/home/softegr/alverson/log_test/"  # Dev path
            try:
                if not self.imagePixmap.isNull():
                    copy(fileName + ".png", path)
                    if self.imageType == "png":
                        copy(fileName + ".ps", path)
                    else:
                        copy(fileName + "." + self.imageType, path)
            
                # Copy .xml file last to ensure images will be picked up by cron job
                # print("Copying file " + fileName + " to path " + path)
                copy(fileName + ".xml", path)
            except IOError as error:
                print(error)
                success = False
            
        return success
    
    def clearForm(self):
        """Clear all form fields (except author)."""
        
        self.logui.titleEntry.clear()
        self.logui.textEntry.clear()

        # Remove all log selection menus except the first
        while self.logMenuCount > 1:
            self.removeLogbook(self.logMenus[-1])


class LogSelectMenu(QWidget):
    '''Menu objects in horizontal layout for selecting logbook facilities'''
    selectedLogs = []
    menuCount = 0
    
    def __init__(self, parent=QVBoxLayout(), initialInstance=True):
        super(LogSelectMenu, self).__init__()
        
        self.parent = parent
        self.logList = {}
        self.initialInstance = initialInstance
        
        self.setupUI()
    
    def setupUI(self):
        '''Create graphical objects for menus.'''
        
        labelSizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        labelSizePolicy.setHorizontalStretch(0)
        labelSizePolicy.setVerticalStretch(0)
        menuSizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        menuSizePolicy.setHorizontalStretch(0)
        menuSizePolicy.setVerticalStretch(0)
        
        logTypeLayout = QHBoxLayout()
        logTypeLayout.setSpacing(0)
        
        typeLabel = QLabel("Log Type:")
        typeLabel.setMinimumSize(QSize(65, 0))
        typeLabel.setMaximumSize(QSize(65, 16777215))
        typeLabel.setSizePolicy(labelSizePolicy)
        logTypeLayout.addWidget(typeLabel)
        self.logType = QComboBox(self)
        self.logType.setMinimumSize(QSize(100, 0))
        self.logType.setMaximumSize(QSize(150, 16777215))
        menuSizePolicy.setHeightForWidth(self.logType.sizePolicy().hasHeightForWidth())
        self.logType.setSizePolicy(menuSizePolicy)
        logTypeLayout.addWidget(self.logType)
        logTypeLayout.setStretch(1, 6)
        
        programLayout = QHBoxLayout()
        programLayout.setSpacing(0)
        
        programLabel = QLabel("Program:")
        programLabel.setMinimumSize(QSize(60, 0))
        programLabel.setMaximumSize(QSize(60, 16777215))
        programLabel.setSizePolicy(labelSizePolicy)
        programLayout.addWidget(programLabel)
        self.programName = QComboBox(self)
        self.programName.setMinimumSize(QSize(100, 0))
        self.programName.setMaximumSize(QSize(150, 16777215))
        menuSizePolicy.setHeightForWidth(self.programName.sizePolicy().hasHeightForWidth())
        self.programName.setSizePolicy(menuSizePolicy)
        programLayout.addWidget(self.programName)
        programLayout.setStretch(1, 6)
        
        # Initial instance allows adding additional menus, all following menus can only remove themselves.
        if self.initialInstance:
            self.logButton = QPushButton("+", self)
            self.logButton.setToolTip("Add logbook")
        else:
            self.logButton = QPushButton("-")
            self.logButton.setToolTip("Remove logbook")
        
        self.logButton.setMinimumSize(QSize(16, 16))  # 24x24
        self.logButton.setMaximumSize(QSize(16, 16))  # 24x24
        self.logButton.setObjectName("roundButton")
        # self.logButton.setAutoFillBackground(True)
        # region = QRegion(QRect(self.logButton.x()+15, self.logButton.y()+14, 20, 20), QRegion.Ellipse)
        # self.logButton.setMask(region)
        
        self.logButton.setStyleSheet("QPushButton {border-radius: 8px;}")
        
        self._logSelectLayout = QHBoxLayout()
        self._logSelectLayout.setSpacing(6)
        self._logSelectLayout.addLayout(logTypeLayout)
        self._logSelectLayout.addLayout(programLayout)
        self._logSelectLayout.addWidget(self.logButton)
        self._logSelectLayout.setStretch(0, 6)
        self._logSelectLayout.setStretch(1, 6)
    
    def _connectSlots(self):
        '''Connect menu change signals.'''
        # QObject.connect(self.logType, SIGNAL("activated(int)"), self.changeLogType)
        QObject.connect(self.logType, SIGNAL("currentIndexChanged(int)"), self.changeLogType)
    
    def show(self):
        '''Display menus and connect even signals.'''
        self.parent.addLayout(self._logSelectLayout)
        self.menuCount += 1
        self._connectSlots()
    
    def selectedType(self):
        return str(self.logType.currentText())
    
    def selectedProgram(self):
        return str(self.programName.currentText())
    
    def addLogbooks(self, type=None, logs=[], default=""):
        '''Add or change list of logbooks.'''
        if type is not None and len(logs) != 0:
            if type in self.logList:
                for logbook in logs:
                    if logbook not in self.logList.get(type)[0]:
                        # print("Adding log " + " to " + type + " log type.")
                        self.logList.get(type)[0].append(logbook)
            else:
                # print("Adding log type: " + type)
                self.logList[type] = []
                self.logList[type].append(logs)
            
            # If default given, auto-select upon menu creation
            if len(self.logList[type]) > 1 and default != "":
                self.logList.get(type)[1] == default
            else:
                self.logList.get(type).append(default)
            
            self.logType.clear()
            self.logType.addItems(list(self.logList.keys()))
            self.changeLogType()
    
    def removeLogbooks(self, type=None, logs=[]):
        '''Remove unwanted logbooks from list.'''
        if type is not None and type in self.logList:
            if len(logs) == 0 or logs == "All":
                del self.logList[type]
            else:
                for logbook in logs:
                    if logbook in self.logList[type]:
                        self.logList[type].remove(logbook)
            
            self.changeLogType()
    
    def changeLogType(self):
        '''Populate log program list to correspond with log type selection.'''
        logType = self.selectedType()
        programs = self.logList.get(logType)[0]
        default = self.logList.get(logType)[1]
        if logType in self.logList:
            self.programName.clear()
            self.programName.addItems(programs)
            self.programName.setCurrentIndex(programs.index(default))
    
    def addMenu(self):
        '''Add menus to parent gui.'''
        self.parent.multiLogLayout.addLayout(self.logSelectLayout)
        self.getPrograms(logType, programName)
    
    def removeLayout(self, layout):
        '''Iteratively remove graphical objects from layout.'''
        for cnt in reversed(range(layout.count())):
            item = layout.takeAt(cnt)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            else:
                '''If sublayout encountered, iterate recursively.'''
                self.removeLayout(item.layout())
    
    def removeMenu(self):
        '''Remove layout from parent gui and destroy object on completion.'''
        self.removeLayout(self._logSelectLayout)
        self.deleteLater()
    

if __name__ == "__main__":
    '''If not spawned by external GUI, launch from localized app'''
    from sys import argv, exit

    app = QApplication(argv)
    
    image = QPixmap()
    deleteOnClose = True
    argnum = len(argv)
    if argnum > 1:
        image = argv[1]
    if argnum >= 2:
        deleteOnClose = argv[2]
    
    log = logbookForm(None, image, "MCC", "MCC", deleteOnClose)
    log.show()

    exit(app.exec_())
