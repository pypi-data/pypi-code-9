"""
Region of interest widget
"""

# Standard library modules.

# Third party modules.
from PySide.QtGui import QLineEdit, QIntValidator

# Local modules.
from pyhmsa.gui.spec.condition.condition import _ConditionWidget

from pyhmsa.spec.condition.region import RegionOfInterest

# Globals and constants variables.

class RegionOfInterestWidget(_ConditionWidget):

    def __init__(self, parent=None):
        _ConditionWidget.__init__(self, RegionOfInterest, parent)

    def _init_ui(self):
        # Widgets
        validator = QIntValidator()
        validator.setBottom(0)

        self._txt_start_channel = QLineEdit()
        self._txt_start_channel.setValidator(validator)
        self._txt_start_channel.setAccessibleName('Start channel')

        self._txt_end_channel = QLineEdit()
        self._txt_end_channel.setValidator(validator)
        self._txt_end_channel.setAccessibleName("End channel")

        # Layouts
        layout = _ConditionWidget._init_ui(self)
        layout.addRow('<i>Start channel</i>', self._txt_start_channel)
        layout.addRow('<i>End channel</i>', self._txt_end_channel)

        # Signals
        self._txt_start_channel.textEdited.connect(self.edited)
        self._txt_end_channel.textEdited.connect(self.edited)

        return layout

    def _create_parameter(self):
        return self.CLASS(0, 1)

    def parameter(self, parameter=None):
        parameter = _ConditionWidget.parameter(self, parameter)
        parameter.channels = (int(self._txt_start_channel.text()),
                              int(self._txt_end_channel.text()))
        return parameter

    def setParameter(self, condition):
        _ConditionWidget.setParameter(self, condition)
        self._txt_start_channel.setText(str(condition.start_channel))
        self._txt_end_channel.setText(str(condition.end_channel))

    def setReadOnly(self, state):
        _ConditionWidget.setReadOnly(self, state)
        self._txt_start_channel.setReadOnly(state)
        self._txt_end_channel.setReadOnly(state)

    def isReadOnly(self):
        return _ConditionWidget.isReadOnly(self) and \
            self._txt_start_channel.isReadOnly() and \
            self._txt_end_channel.isReadOnly()

    def hasAcceptableInput(self):
        return _ConditionWidget.hasAcceptableInput(self) and \
            self._txt_start_channel.hasAcceptableInput() and \
            self._txt_end_channel.hasAcceptableInput()
