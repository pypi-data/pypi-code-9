
# Copyright (c) 2009 - 2015, UChicago Argonne, LLC.
# See LICENSE file for details.

'''
show the About box
'''

import os, sys
on_rtd = os.environ.get('READTHEDOCS', None) == 'True'
if on_rtd:
    from mock_PyQt4 import QtCore, QtGui
else:
    from PyQt4 import QtCore, QtGui

import __init__
import history
import plainTextEdit
import resources

UI_FILE = 'about.ui'
DOCS_URL = 'http://Assign_GUP.readthedocs.org'
LICENSE_FILE = 'LICENSE'


class InfoBox(QtGui.QDialog):
    '''
    a Qt GUI for the About box
    '''

    def __init__(self, parent=None, settings=None):
        self.settings = settings
        QtGui.QDialog.__init__(self, parent)
        resources.loadUi(UI_FILE, baseinstance=self)
        
        self.version.setText('software version: ' + str(__init__.__version__))

        self.docs_pb.clicked.connect(self.doUrl)
        self.license_pb.clicked.connect(self.doLicense)

    def doUrl(self):
        '''opening documentation URL in default browser'''
        history.addLog('opening documentation URL in default browser')
        url = QtCore.QUrl(DOCS_URL)
        service = QtGui.QDesktopServices()
        service.openUrl(url)

    def doLicense(self):
        '''show the license'''
        history.addLog('opening License in new window')
        license_text = open(resources.resource_file('../' + LICENSE_FILE), 'r').read()
        ui = plainTextEdit.TextWindow(self, 'LICENSE', license_text, self.settings)
        ui.setMinimumSize(700, 500)
        ui.setWindowModality(QtCore.Qt.ApplicationModal)
        ui.show()
