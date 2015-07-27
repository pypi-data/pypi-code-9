"""
Specimen conditions widgets
"""

# Standard library modules.

# Third party modules.

# Local modules.
from pyhmsa.gui.util.parameter import \
    TextAttributeLineEdit, NumericalAttributeLineEdit
from pyhmsa.gui.spec.condition.condition import _ConditionWidget
from pyhmsa.gui.spec.condition.composition import CompositionElementalWidget

from pyhmsa.spec.condition.specimen import Specimen

# Globals and constants variables.

class SpecimenWidget(_ConditionWidget):

    def __init__(self, parent=None):
        _ConditionWidget.__init__(self, Specimen, parent)

    def _init_ui(self):
        # Widgets
        self._txt_name = TextAttributeLineEdit(self.CLASS.name)
        self._txt_description = TextAttributeLineEdit(self.CLASS.description)
        self._txt_origin = TextAttributeLineEdit(self.CLASS.origin)
        self._txt_formula = TextAttributeLineEdit(self.CLASS.formula)
        self._wdg_composition = CompositionElementalWidget()
        self._txt_temperature = NumericalAttributeLineEdit(self.CLASS.temperature)

        # Layouts
        layout = _ConditionWidget._init_ui(self)
        layout.addRow('<i>Name</i>', self._txt_name)
        layout.addRow('Description', self._txt_description)
        layout.addRow('Origin', self._txt_origin)
        layout.addRow('Formula', self._txt_formula)
        layout.addRow('Composition', self._wdg_composition)
        layout.addRow('Temperature', self._txt_temperature)

        # Signals
        self._txt_name.textEdited.connect(self.edited)
        self._txt_description.textEdited.connect(self.edited)
        self._txt_origin.textEdited.connect(self.edited)
        self._txt_formula.textEdited.connect(self.edited)
        self._wdg_composition.edited.connect(self.edited)
        self._txt_temperature.textEdited.connect(self.edited)

        return layout

    def _create_parameter(self):
        return self.CLASS('dummy')

    def parameter(self, parameter=None):
        parameter = _ConditionWidget.parameter(self, parameter)
        parameter.name = self._txt_name.text()
        parameter.description = self._txt_description.text()
        parameter.origin = self._txt_origin.text()
        parameter.formula = self._txt_formula.text()
        parameter.composition = self._wdg_composition.condition()
        parameter.temperature = self._txt_temperature.text()
        return parameter

    def setParameter(self, condition):
        _ConditionWidget.setParameter(self, condition)
        self._txt_name.setText(condition.name)
        self._txt_description.setText(condition.description)
        self._txt_origin.setText(condition.origin)
        self._txt_formula.setText(condition.formula)
        self._wdg_composition.setCondition(condition.composition)
        self._txt_temperature.setText(condition.temperature)

    def setReadOnly(self, state):
        _ConditionWidget.setReadOnly(self, state)
        self._txt_name.setReadOnly(state)
        self._txt_description.setReadOnly(state)
        self._txt_origin.setReadOnly(state)
        self._txt_formula.setReadOnly(state)
        self._wdg_composition.setReadOnly(state)
        self._txt_temperature.setReadOnly(state)

    def isReadOnly(self):
        return _ConditionWidget.isReadOnly(self) and \
            self._txt_name.isReadOnly() and \
            self._txt_description.isReadOnly() and \
            self._txt_origin.isReadOnly() and \
            self._txt_formula.isReadOnly() and \
            self._wdg_composition.isReadOnly() and \
            self._txt_temperature.isReadOnly()

    def hasAcceptableInput(self):
        return _ConditionWidget.hasAcceptableInput(self) and \
            self._txt_name.hasAcceptableInput() and \
            self._txt_description.hasAcceptableInput() and \
            self._txt_origin.hasAcceptableInput() and \
            self._txt_formula.hasAcceptableInput() and \
            self._wdg_composition.hasAcceptableInput() and \
            self._txt_temperature.hasAcceptableInput()
