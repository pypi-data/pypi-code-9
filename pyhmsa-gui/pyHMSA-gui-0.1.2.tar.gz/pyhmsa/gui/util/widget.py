"""
Custom widgets
"""

# Standard library modules.

# Third party modules.
from PySide.QtCore import QSize, Qt
from PySide.QtGui import \
    (QWidget, QPushButton, QVBoxLayout, QSizePolicy, QPainter, QBrush,
     QColorDialog)

# Local modules.

# Globals and constants variables.

class ColorDialogButton(QWidget):

    class _ColorButton(QPushButton):

        def __init__(self, *args, **kwargs):
            QPushButton.__init__(self, *args, **kwargs)

            # Variables
            self._color = Qt.red
            self._padding = 5

        def setColor(self, color):
            self._color = color

        def color(self):
            return self._color

        def setPadding(self, pad):
            self._padding = int(pad)

        def padding(self):
            return self._padding

        def paintEvent(self, event):
            QPushButton.paintEvent(self, event)

            color = self.color()
            padding = self.padding()

            rect = event.rect()
            painter = QPainter()
            painter.begin(self)
            painter.setBrush(QBrush(color))
            painter.setPen(Qt.NoPen)
            rect.adjust(padding, padding, -1 - padding, -1 - padding)
            painter.drawRect(rect)
            painter.end()

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        # Variables
        self._color = Qt.red

        # Widgets
        self._button = self._ColorButton()
        self._button.setFixedSize(QSize(25, 25))
        self._button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # Layouts
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._button)
        self.setLayout(layout)

        # Signals
        self._button.clicked.connect(self._on_clicked)

        # Defaults
        self.setColor(Qt.red)

    def _on_clicked(self):
        dialog = QColorDialog(self.color())
        if not dialog.exec_():
            return
        self.setColor(dialog.selectedColor())

    def setColor(self, color):
        self._button.setColor(color)

    def color(self):
        return self._button.color()
