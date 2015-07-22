import sys
import os as _os
on_rtd = _os.environ.get('READTHEDOCS', None) == 'True'
if not on_rtd:
    from PyQt4 import QtGui


def get_app(argv=sys.argv):
    global app
    app = QtGui.QApplication.instance()
    if not app:
        app = QtGui.QApplication(argv)
    return app
