"""
Instrument widget
"""

# Standard library modules.

# Third party modules.

# Local modules.
from pyhmsa.gui.spec.condition.condition import _ConditionWidget
from pyhmsa.gui.util.parameter import TextAttributeLineEdit

from pyhmsa.spec.condition.instrument import Instrument

# Globals and constants variables.

class InstrumentWidget(_ConditionWidget):

    def __init__(self, parent=None):
        _ConditionWidget.__init__(self, Instrument, parent)

    def _init_ui(self):
        # Controls
        self._txt_manufacturer = TextAttributeLineEdit(self.CLASS.manufacturer)
        self._txt_model = TextAttributeLineEdit(self.CLASS.model)
        self._txt_serial_number = TextAttributeLineEdit(self.CLASS.serial_number)

        # Layouts
        layout = _ConditionWidget._init_ui(self)
        layout.addRow("<i>Manufacturer</i>", self._txt_manufacturer)
        layout.addRow("<i>Model</i>", self._txt_model)
        layout.addRow("Serial number", self._txt_serial_number)

        # Signals
        self._txt_manufacturer.textEdited.connect(self.edited)
        self._txt_model.textEdited.connect(self.edited)
        self._txt_serial_number.textEdited.connect(self.edited)

        return layout

    def _create_parameter(self):
        return self.CLASS('manufacturer', 'model')

    def parameter(self, parameter=None):
        parameter = _ConditionWidget.parameter(self, parameter)
        parameter.manufacturer = self._txt_manufacturer.text()
        parameter.model = self._txt_model.text()
        parameter.serial_number = self._txt_serial_number.text()
        return parameter

    def setParameter(self, condition):
        _ConditionWidget.setParameter(self, condition)
        self._txt_manufacturer.setText(condition.manufacturer)
        self._txt_model.setText(condition.model)
        self._txt_serial_number.setText(condition.serial_number)

    def setReadOnly(self, state):
        _ConditionWidget.setReadOnly(self, state)
        self._txt_manufacturer.setReadOnly(state)
        self._txt_model.setReadOnly(state)
        self._txt_serial_number.setReadOnly(state)

    def isReadOnly(self):
        return _ConditionWidget.isReadOnly(self) and \
            self._txt_manufacturer.isReadOnly() and \
            self._txt_model.isReadOnly() and \
            self._txt_serial_number.isReadOnly()

    def hasAcceptableInput(self):
        return _ConditionWidget.hasAcceptableInput(self) and \
            self._txt_manufacturer.hasAcceptableInput() and \
            self._txt_model.hasAcceptableInput() and \
            self._txt_serial_number.hasAcceptableInput()


