"""
Elemend ID widget
"""

# Standard library modules.

# Third party modules.

# Local modules.
from pyhmsa.gui.spec.condition.condition import _ConditionWidget
from pyhmsa.gui.util.parameter import \
    (AtomicNumberAttributePushButton, TextAttributeLineEdit,
     NumericalAttributeLineEdit)

from pyhmsa.spec.condition.elementalid import ElementalID, ElementalIDXray

# Globals and constants variables.

class ElementalIDWidget(_ConditionWidget):

    def __init__(self, parent=None):
        _ConditionWidget.__init__(self, ElementalID, parent)

    def _init_ui(self):
        # Widgets
        self._btn_atomic_number = AtomicNumberAttributePushButton(self.CLASS.atomic_number)

        # Layouts
        layout = _ConditionWidget._init_ui(self)
        layout.addRow('<i>Element</i>', self._btn_atomic_number)

        # Signals
        self._btn_atomic_number.selectionChanged.connect(self.edited)

        return layout

    def _create_parameter(self):
        return self.CLASS(1)

    def parameter(self, parameter=None):
        parameter = _ConditionWidget.parameter(self, parameter)
        parameter.atomic_number = self._btn_atomic_number.atomicNumber()
        return parameter

    def setParameter(self, condition):
        _ConditionWidget.setParameter(self, condition)
        self._btn_atomic_number.setAtomicNumber(condition.atomic_number)

    def setReadOnly(self, state):
        _ConditionWidget.setReadOnly(self, state)
        self._btn_atomic_number.setEnabled(not state)

    def isReadOnly(self):
        return _ConditionWidget.isReadOnly(self) and \
            not self._btn_atomic_number.isEnabled()

class ElementalIDXrayWidget(ElementalIDWidget):

    def __init__(self, parent=None):
        _ConditionWidget.__init__(self, ElementalIDXray, parent)

    def _init_ui(self):
        # Widgets
        self._txt_line = TextAttributeLineEdit(self.CLASS.line)
        self._txt_energy = NumericalAttributeLineEdit(self.CLASS.energy)

        # Layouts
        layout = ElementalIDWidget._init_ui(self)
        layout.addRow('<i>Line</i>', self._txt_line)
        layout.addRow('Energy', self._txt_energy)

        # Signals
        self._txt_line.textEdited.connect(self.edited)
        self._txt_energy.textEdited.connect(self.edited)

        return layout

    def _create_parameter(self):
        return self.CLASS(1, 'Ka')

    def parameter(self, parameter=None):
        parameter = ElementalIDWidget.parameter(self, parameter)
        parameter.line = self._txt_line.text()
        parameter.energy = self._txt_energy.text()
        return parameter

    def setParameter(self, condition):
        ElementalIDWidget.setParameter(self, condition)
        self._txt_line.setText(condition.line)
        self._txt_energy.setText(condition.energy)

    def setReadOnly(self, state):
        ElementalIDWidget.setReadOnly(self, state)
        self._txt_line.setReadOnly(state)
        self._txt_energy.setReadOnly(state)

    def isReadOnly(self):
        return ElementalIDWidget.isReadOnly(self) and \
            self._txt_line.isReadOnly() and \
            self._txt_energy.isReadOnly()

    def hasAcceptableInput(self):
        return ElementalIDWidget.hasAcceptableInput(self) and \
            self._txt_line.hasAcceptableInput() and \
            self._txt_energy.hasAcceptableInput()
