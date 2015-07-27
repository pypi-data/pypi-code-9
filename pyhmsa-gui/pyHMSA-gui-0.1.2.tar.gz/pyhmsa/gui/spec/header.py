"""
Header widget
"""

# Standard library modules.

# Third party modules.
from PySide.QtGui import QDateEdit, QTimeEdit
from PySide.QtCore import QDate, QTime

# Local modules.
from pyhmsa.gui.util.parameter import ParameterWidget, TextAttributeLineEdit

from pyhmsa.spec.header import Header

# Globals and constants variables.

class HeaderWidget(ParameterWidget):

    def __init__(self, parent=None):
        ParameterWidget.__init__(self, Header, parent)

    def _init_ui(self):
        # Widgets
        self._txt_title = TextAttributeLineEdit(self.CLASS.title)
        self._txt_author = TextAttributeLineEdit(self.CLASS.author)
        self._txt_owner = TextAttributeLineEdit(self.CLASS.owner)
        self._txt_date = QDateEdit()
        self._txt_date.setDisplayFormat('yyyy-MM-dd')
        self._txt_time = QTimeEdit()
        self._txt_time.setDisplayFormat('hh:mm:ss')
        self._txt_timezone = TextAttributeLineEdit(self.CLASS.timezone)
        self._txt_checksum = TextAttributeLineEdit(self.CLASS.checksum)
        self._txt_checksum.setReadOnly(True)

        # Layouts
        layout = ParameterWidget._init_ui(self)
        layout.addRow('Title', self._txt_title)
        layout.addRow('Author', self._txt_author)
        layout.addRow('Owner', self._txt_owner)
        layout.addRow('Date', self._txt_date)
        layout.addRow('Time', self._txt_time)
        layout.addRow('Timezone', self._txt_timezone)
        layout.addRow('Checksum', self._txt_checksum)

        # Signals
        self._txt_title.textEdited.connect(self.edited)
        self._txt_author.textEdited.connect(self.edited)
        self._txt_owner.textEdited.connect(self.edited)
        self._txt_date.dateChanged.connect(self.edited)
        self._txt_time.timeChanged.connect(self.edited)
        self._txt_timezone.textEdited.connect(self.edited)
        self._txt_checksum.textEdited.connect(self.edited)

        return layout

    def parameter(self, parameter=None):
        parameter = ParameterWidget.parameter(self, parameter)
        parameter.title = self._txt_title.text()
        parameter.author = self._txt_author.text()
        parameter.owner = self._txt_owner.text()
        parameter.date = self._txt_date.date().toString('yyyy-MM-dd')
        parameter.time = self._txt_time.time().toString('hh:mm:ss')
        parameter.timezone = self._txt_timezone.text()
        return parameter

    def setParameter(self, header):
        ParameterWidget.setParameter(self, header)
        self._txt_title.setText(header.title)
        self._txt_author.setText(header.author)
        self._txt_owner.setText(header.owner)
        date = header.date
        if date is not None:
            self._txt_date.setDate(QDate(date.year, date.month, date.day))
        time = header.time
        if time is not None:
            self._txt_time.setTime(QTime(time.hour, time.minute, time.second))
        self._txt_timezone.setText(header.timezone)
        checksum = header.checksum
        if checksum is not None:
            self._txt_checksum.setText(checksum.value)

    def header(self, header=None):
        return self.parameter(header)

    def setHeader(self, header):
        self.setParameter(header)

    def setReadOnly(self, state):
        ParameterWidget.setReadOnly(self, state)
        self._txt_title.setReadOnly(state)
        self._txt_author.setReadOnly(state)
        self._txt_owner.setReadOnly(state)
        self._txt_date.setReadOnly(state)
        self._txt_time.setReadOnly(state)
        self._txt_timezone.setReadOnly(state)
        self._txt_checksum.setReadOnly(state)

    def isReadOnly(self):
        return ParameterWidget.isReadOnly(self) and \
            self._txt_title.isReadOnly() and \
            self._txt_author.isReadOnly() and \
            self._txt_owner.isReadOnly() and \
            self._txt_date.isReadOnly() and \
            self._txt_time.isReadOnly() and \
            self._txt_timezone.isReadOnly() and \
            self._txt_checksum.isReadOnly()

    def hasAcceptableInput(self):
        return ParameterWidget.hasAcceptableInput(self) and \
            self._txt_title.hasAcceptableInput() and \
            self._txt_author.hasAcceptableInput() and \
            self._txt_owner.hasAcceptableInput() and \
            self._txt_date.hasAcceptableInput() and \
            self._txt_time.hasAcceptableInput() and \
            self._txt_timezone.hasAcceptableInput() and \
            self._txt_checksum.hasAcceptableInput()
