'''
execute this file for opening guiSAXS qt (the graphic user interface for pySAXS)
'''
from PyQt4 import QtGui,QtCore
import sys
app = QtGui.QApplication(sys.argv)
splash_pix = QtGui.QPixmap('splash.png')
splash = QtGui.QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)
splash.setMask(splash_pix.mask())
splash.show()
app.processEvents()
      
from pySAXS.guisaxs.qt import mainGuisaxs    
myapp = mainGuisaxs.mainGuisaxs()
myapp.show()
splash.destroy()
sys.exit(app.exec_())