"""
Validation utilities.
"""

# Standard library modules.

# Third party modules.
from PySide.QtGui import QMessageBox

# Local modules.

# Globals and constants variables.

def validate_widget(*widgets):
    invalids = []
    for widget in widgets:
        _validate_widget_recursive(widget, invalids)

    if not invalids:
        return True

    if len(invalids) >= 2:
        message = 'The following fields contain error(s):\n'
        title = 'Validation errors'
    else:
        message = 'The following field contains error(s):\n'
        title = 'Validation error'

    for invalid_widget in invalids:
        message += '- %s\n' % invalid_widget.accessibleName()

    QMessageBox.critical(widget.parent(), title, message)
    return False

def _validate_widget_recursive(widget, invalids):
    if hasattr(widget, 'hasAcceptableInput') and \
            not widget.hasAcceptableInput() and \
            widget.isVisible():
        invalids.append(widget)

    for child in widget.children():
        _validate_widget_recursive(child, invalids)
