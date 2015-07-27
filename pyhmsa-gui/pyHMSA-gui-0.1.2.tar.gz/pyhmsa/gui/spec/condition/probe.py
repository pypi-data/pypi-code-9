"""
Probe widgets
"""

# Standard library modules.

# Third party modules.
from PySide.QtGui import QComboBox

# Local modules.
from pyhmsa.gui.spec.condition.condition import _ConditionWidget
from pyhmsa.gui.util.parameter import NumericalAttributeLineEdit

from pyhmsa.spec.condition.probe import ProbeEM, ProbeTEM

# Globals and constants variables.
from pyhmsa.spec.condition.probe import _GUN_TYPES, _LENS_MODES, LENS_MODE_IMAGE

class ProbeEMWidget(_ConditionWidget):

    def __init__(self, parent=None):
        _ConditionWidget.__init__(self, ProbeEM, parent)

    def _init_ui(self):
        # Widgets
        self._txt_beam_voltage = NumericalAttributeLineEdit(self.CLASS.beam_voltage)
        self._txt_beam_current = NumericalAttributeLineEdit(self.CLASS.beam_current)
        self._cb_gun_type = QComboBox()
        self._cb_gun_type.addItems([None] + list(_GUN_TYPES))
        self._txt_emission_current = NumericalAttributeLineEdit(self.CLASS.emission_current)
        self._txt_filament_current = NumericalAttributeLineEdit(self.CLASS.filament_current)
        self._txt_extractor_bias = NumericalAttributeLineEdit(self.CLASS.extractor_bias)
        self._txt_beam_diameter = NumericalAttributeLineEdit(self.CLASS.beam_diameter)
        self._txt_chamber_pressure = NumericalAttributeLineEdit(self.CLASS.chamber_pressure)
        self._txt_gun_pressure = NumericalAttributeLineEdit(self.CLASS.gun_pressure)
        self._txt_scan_magnification = NumericalAttributeLineEdit(self.CLASS.scan_magnification)
        self._txt_scan_magnification.setFormat('{0:d}')
        self._txt_working_distance = NumericalAttributeLineEdit(self.CLASS.working_distance)

        # Layout
        layout = _ConditionWidget._init_ui(self)
        layout.addRow('<i>Beam voltage</i>', self._txt_beam_voltage)
        layout.addRow('Beam current', self._txt_beam_current)
        layout.addRow('Type of gun', self._cb_gun_type)
        layout.addRow('Emission current', self._txt_emission_current)
        layout.addRow('Filament current', self._txt_filament_current)
        layout.addRow('Extractor bias', self._txt_extractor_bias)
        layout.addRow('Beam diameter', self._txt_beam_diameter)
        layout.addRow('Chamber pressure', self._txt_chamber_pressure)
        layout.addRow('Gun pressure', self._txt_gun_pressure)
        layout.addRow('Scan magnification', self._txt_scan_magnification)
        layout.addRow('Working distance', self._txt_working_distance)

        # Signals
        self._txt_beam_voltage.textEdited.connect(self.edited)
        self._txt_beam_current.textEdited.connect(self.edited)
        self._cb_gun_type.currentIndexChanged.connect(self.edited)
        self._txt_emission_current.textEdited.connect(self.edited)
        self._txt_filament_current.textEdited.connect(self.edited)
        self._txt_extractor_bias.textEdited.connect(self.edited)
        self._txt_beam_diameter.textEdited.connect(self.edited)
        self._txt_chamber_pressure.textEdited.connect(self.edited)
        self._txt_gun_pressure.textEdited.connect(self.edited)
        self._txt_scan_magnification.textEdited.connect(self.edited)
        self._txt_working_distance.textEdited.connect(self.edited)

        return layout

    def _create_parameter(self):
        return self.CLASS(1e3)

    def parameter(self, parameter=None):
        parameter = _ConditionWidget.parameter(self, parameter)
        parameter.beam_voltage = self._txt_beam_voltage.text()
        parameter.beam_current = self._txt_beam_current.text()
        parameter.gun_type = self._cb_gun_type.currentText()
        parameter.emission_current = self._txt_emission_current.text()
        parameter.filament_current = self._txt_filament_current.text()
        parameter.extractor_bias = self._txt_extractor_bias.text()
        parameter.beam_diameter = self._txt_beam_diameter.text()
        parameter.chamber_pressure = self._txt_chamber_pressure.text()
        parameter.gun_pressure = self._txt_gun_pressure.text()
        parameter.scan_magnification = self._txt_scan_magnification.text()
        parameter.working_distance = self._txt_working_distance.text()
        return parameter

    def setParameter(self, condition):
        _ConditionWidget.setParameter(self, condition)
        self._txt_beam_voltage.setText(condition.beam_voltage)
        self._txt_beam_current.setText(condition.beam_current)
        self._cb_gun_type.setCurrentIndex(self._cb_gun_type.findText(condition.gun_type))
        self._txt_emission_current.setText(condition.emission_current)
        self._txt_filament_current.setText(condition.filament_current)
        self._txt_extractor_bias.setText(condition.extractor_bias)
        self._txt_beam_diameter.setText(condition.beam_diameter)
        self._txt_chamber_pressure.setText(condition.chamber_pressure)
        self._txt_gun_pressure.setText(condition.gun_pressure)
        self._txt_scan_magnification.setText(condition.scan_magnification)
        self._txt_working_distance.setText(condition.working_distance)

    def setReadOnly(self, state):
        _ConditionWidget.setReadOnly(self, state)
        self._txt_beam_voltage.setReadOnly(state)
        self._txt_beam_current.setReadOnly(state)
        self._cb_gun_type.setEnabled(not state)
        self._txt_emission_current.setReadOnly(state)
        self._txt_filament_current.setReadOnly(state)
        self._txt_extractor_bias.setReadOnly(state)
        self._txt_beam_diameter.setReadOnly(state)
        self._txt_chamber_pressure.setReadOnly(state)
        self._txt_gun_pressure.setReadOnly(state)
        self._txt_scan_magnification.setReadOnly(state)
        self._txt_working_distance.setReadOnly(state)

    def isReadOnly(self):
        return _ConditionWidget.isReadOnly(self) and \
            self._txt_beam_voltage.isReadOnly() and \
            self._txt_beam_current.isReadOnly() and \
            not self._cb_gun_type.isEnabled() and \
            self._txt_emission_current.isReadOnly() and \
            self._txt_filament_current.isReadOnly() and \
            self._txt_extractor_bias.isReadOnly() and \
            self._txt_beam_diameter.isReadOnly() and \
            self._txt_chamber_pressure.isReadOnly() and \
            self._txt_gun_pressure.isReadOnly() and \
            self._txt_scan_magnification.isReadOnly() and \
            self._txt_working_distance.isReadOnly()

    def hasAcceptableInput(self):
        return _ConditionWidget.hasAcceptableInput(self) and \
            self._txt_beam_voltage.hasAcceptableInput() and \
            self._txt_beam_current.hasAcceptableInput() and \
            self._txt_emission_current.hasAcceptableInput() and \
            self._txt_filament_current.hasAcceptableInput() and \
            self._txt_extractor_bias.hasAcceptableInput() and \
            self._txt_beam_diameter.hasAcceptableInput() and \
            self._txt_chamber_pressure.hasAcceptableInput() and \
            self._txt_gun_pressure.hasAcceptableInput() and \
            self._txt_scan_magnification.hasAcceptableInput() and \
            self._txt_working_distance.hasAcceptableInput()

class ProbeTEMWidget(ProbeEMWidget):

    def __init__(self, parent=None):
        _ConditionWidget.__init__(self, ProbeTEM, parent)

    def _init_ui(self):
        # Controls
        self._cb_lens_mode = QComboBox()
        self._cb_lens_mode.addItems(list(_LENS_MODES))
        self._txt_camera_magnification = NumericalAttributeLineEdit(self.CLASS.camera_magnification)
        self._txt_convergence_angle = NumericalAttributeLineEdit(self.CLASS.convergence_angle)

        # Layouts
        layout = ProbeEMWidget._init_ui(self)
        layout.insertRow(1, '<i>Lens mode</i>', self._cb_lens_mode)
        layout.addRow('Camera magnification', self._txt_camera_magnification)
        layout.addRow('Convergence angle', self._txt_convergence_angle)

        # Signals
        self._cb_lens_mode.currentIndexChanged.connect(self.edited)
        self._txt_camera_magnification.textEdited.connect(self.edited)
        self._txt_convergence_angle.textEdited.connect(self.edited)

        return layout

    def _create_parameter(self):
        return self.CLASS(1e3, LENS_MODE_IMAGE)

    def parameter(self, parameter=None):
        parameter = ProbeEMWidget.parameter(self, parameter)
        parameter.lens_mode = self._cb_lens_mode.currentText()
        parameter.camera_magnification = self._txt_camera_magnification.text()
        parameter.convergence_angle = self._txt_convergence_angle.text()
        return parameter

    def setParameter(self, condition):
        ProbeEMWidget.setParameter(self, condition)
        self._cb_lens_mode.setCurrentIndex(self._cb_lens_mode.findText(condition.lens_mode))
        self._txt_camera_magnification.setText(condition.camera_magnification)
        self._txt_convergence_angle.setText(condition.convergence_angle)

    def setReadOnly(self, state):
        ProbeEMWidget.setReadOnly(self, state)
        self._cb_lens_mode.setEnabled(not state)
        self._txt_camera_magnification.setReadOnly(state)
        self._txt_convergence_angle.setReadOnly(state)

    def isReadOnly(self):
        return ProbeEMWidget.isReadOnly(self) and \
            not self._cb_lens_mode.isEnabled() and \
            self._txt_camera_magnification.isReadOnly() and \
            self._txt_convergence_angle.isReadOnly()

    def hasAcceptableInput(self):
        return ProbeEMWidget.hasAcceptableInput(self) and \
            self._txt_camera_magnification.hasAcceptableInput() and \
            self._txt_convergence_angle.hasAcceptableInput()
