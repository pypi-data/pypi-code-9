"""
Layout utilities
"""

# Standard library modules.

# Third party modules.
from PySide.QtGui import QHBoxLayout, QFormLayout, QLayout

# Local modules.

# Globals and constants variables.

def horizontal(*widgets):
    layout = QHBoxLayout()
    for widget in widgets:
        layout.addWidget(widget)
    return layout

def align_form(layout):
    layouts = []
    _find_layout(layout, QFormLayout, layouts)

    labels = []
    for layout in layouts:
        for index in range(layout.count()):
            layoutitem = layout.itemAt(index, QFormLayout.ItemRole.LabelRole)
            if layoutitem is not None and layoutitem.widget() is not None:
                labels.append(layoutitem.widget())

    maxwidth = float('-inf')
    for label in labels:
        maxwidth = max(maxwidth, label.sizeHint().width())

    for label in labels:
        label.setMinimumSize(maxwidth, 0)

def _find_layout(layout, clasz, layouts):
    for item in map(layout.itemAt, range(layout.count())):
        if isinstance(item, QLayout):
            _find_layout(item, clasz, layouts)
        else:
            if item.widget() is not None and item.widget().layout() is not None:
                _find_layout(item.widget().layout(), clasz, layouts)

    if isinstance(layout, clasz):
        layouts.append(layout)
