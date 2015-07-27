"""
Special message box
"""

# Standard library modules.
import sys
import traceback
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

# Third party modules.
from PySide.QtGui import QMessageBox

# Local modules.

# Globals and constants variables.

def exception(parent, ex, buttons=QMessageBox.Ok,
              defaultButton=QMessageBox.NoButton):
    title = type(ex).__name__
    message = str(ex)
    tb = StringIO()
    if hasattr(ex, '__traceback__'):
        exc_traceback = ex.__traceback__
    else:
        exc_traceback = sys.exc_info()[2]
    traceback.print_tb(exc_traceback, file=tb)

    msgbox = QMessageBox(QMessageBox.Icon.Critical, title, message, buttons, parent)
    msgbox.setDefaultButton(defaultButton)
    msgbox.setDetailedText(tb.getvalue())
    msgbox.exec_()

def exceptions(parent, exs, buttons=QMessageBox.Ok,
              defaultButton=QMessageBox.NoButton):
    title = 'Exception(s)'
    message = '\n'.join(map(str, exs))

    tracebacks = []
    for ex in exs:
        tb = StringIO()
        if not hasattr(ex, '__traceback__'):
            continue
        exc_traceback = ex.__traceback__
        traceback.print_tb(exc_traceback, file=tb)
        tracebacks.append(tb.getvalue())

    msgbox = QMessageBox(QMessageBox.Icon.Critical, title, message, buttons, parent)
    msgbox.setDefaultButton(defaultButton)
    msgbox.setDetailedText('\n'.join(tracebacks))
    msgbox.exec_()
