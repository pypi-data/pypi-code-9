"""
Acquisition conditions widgets
"""

# Standard library modules.

# Third party modules.
from PySide.QtGui import QComboBox

# Local modules.
from pyhmsa.gui.util.parameter import NumericalAttributeLineEdit
from pyhmsa.gui.spec.condition.condition import _ConditionWidget
from pyhmsa.gui.spec.condition.specimenposition import \
    SpecimenPositionWidget, SpecimenPositionListWidget

from pyhmsa.spec.condition.acquisition import \
    (AcquisitionPoint, AcquisitionMultipoint, AcquisitionRasterLinescan,
     AcquisitionRasterXY, AcquisitionRasterXYZ)
from pyhmsa.spec.condition.specimenposition import SpecimenPosition

# Globals and constants variables.
from pyhmsa.spec.condition.acquisition import \
    _RASTER_MODES, _POSITION_LOCATIONS, _RASTER_MODES_Z

class _AcquisitionWidget(_ConditionWidget):

    def _init_ui(self):
        # Widgets
        self._txt_dwell_time = NumericalAttributeLineEdit(self.CLASS.dwell_time)
        self._txt_total_time = NumericalAttributeLineEdit(self.CLASS.total_time)
        self._txt_dwell_time_live = NumericalAttributeLineEdit(self.CLASS.dwell_time_live)

        # Layouts
        layout = _ConditionWidget._init_ui(self)
        layout.addRow('Dwell time', self._txt_dwell_time)
        layout.addRow('Total time', self._txt_total_time)
        layout.addRow('Dwell time (live)', self._txt_dwell_time_live)

        # Signals
        self._txt_dwell_time.textEdited.connect(self.edited)
        self._txt_total_time.textEdited.connect(self.edited)
        self._txt_dwell_time_live.textEdited.connect(self.edited)

        return layout

    def parameter(self, parameter=None):
        parameter = _ConditionWidget.parameter(self, parameter)
        parameter.dwell_time = self._txt_dwell_time.text()
        parameter.total_time = self._txt_total_time.text()
        parameter.dwell_time_live = self._txt_dwell_time_live.text()
        return parameter

    def setParameter(self, condition):
        _ConditionWidget.setParameter(self, condition)
        self._txt_dwell_time.setText(condition.dwell_time)
        self._txt_total_time.setText(condition.total_time)
        self._txt_dwell_time_live.setText(condition.dwell_time_live)

    def setReadOnly(self, state):
        _ConditionWidget.setReadOnly(self, state)
        self._txt_dwell_time.setReadOnly(state)
        self._txt_total_time.setReadOnly(state)
        self._txt_dwell_time_live.setReadOnly(state)

    def isReadOnly(self):
        return _ConditionWidget.isReadOnly(self) and \
            self._txt_dwell_time.isReadOnly() and \
            self._txt_total_time.isReadOnly() and \
            self._txt_dwell_time_live.isReadOnly()

    def hasAcceptableInput(self):
        return _ConditionWidget.hasAcceptableInput(self) and \
            self._txt_dwell_time.hasAcceptableInput() and \
            self._txt_total_time.hasAcceptableInput() and \
            self._txt_dwell_time_live.hasAcceptableInput()

class AcquisitionPointWidget(_AcquisitionWidget):

    def __init__(self, parent=None):
        _AcquisitionWidget.__init__(self, AcquisitionPoint, parent)

    def _init_ui(self):
        # Widgets
        self._wdg_position = SpecimenPositionWidget(inline=True)

        # Layouts
        layout = _AcquisitionWidget._init_ui(self)
        layout.insertRow(0, 'Position', self._wdg_position)

        # Signals
        self._wdg_position.edited.connect(self.edited)

        return layout

    def _create_parameter(self):
        return self.CLASS(position=SpecimenPosition())

    def parameter(self, parameter=None):
        parameter = _AcquisitionWidget.parameter(self, parameter)
        parameter.position = self._wdg_position.condition()
        return parameter

    def setParameter(self, condition):
        _AcquisitionWidget.setParameter(self, condition)
        if condition.position is not None:
            self._wdg_position.setParameter(condition.position)

    def setReadOnly(self, state):
        _AcquisitionWidget.setReadOnly(self, state)
        self._wdg_position.setReadOnly(state)

    def isReadOnly(self):
        return _AcquisitionWidget.isReadOnly(self) and \
            self._wdg_position.isReadOnly()

    def hasAcceptableInput(self):
        return _AcquisitionWidget.hasAcceptableInput(self) and \
            self._wdg_position.hasAcceptableInput()

class AcquisitionMultipointWidget(_AcquisitionWidget):

    def __init__(self, parent=None):
        _AcquisitionWidget.__init__(self, AcquisitionMultipoint, parent)

    def _init_ui(self):
        # Widgets
        self._wdg_positions = SpecimenPositionListWidget()

        # Layouts
        layout = _AcquisitionWidget._init_ui(self)
        layout.addRow('Positions', self._wdg_positions)

        # Signals
        self._wdg_positions.edited.connect(self.edited)

        return layout

    def parameter(self, parameter=None):
        parameter = _AcquisitionWidget.parameter(self, parameter)
        parameter.positions.clear()
        parameter.positions.extend(self._wdg_positions.positions())
        return parameter

    def setParameter(self, condition):
        _AcquisitionWidget.setParameter(self, condition)
        self._wdg_positions.setPositions(condition.positions)

    def setReadOnly(self, state):
        _AcquisitionWidget.setReadOnly(self, state)
        self._wdg_positions.setReadOnly(state)

    def isReadOnly(self):
        return _AcquisitionWidget.isReadOnly(self) and \
            self._wdg_positions.isReadOnly()

    def hasAcceptableInput(self):
        return _AcquisitionWidget.hasAcceptableInput(self) and \
            self._wdg_positions.hasAcceptableInput()

class _AcquisitionRasterWidget(_AcquisitionWidget):

    def _init_ui(self):
        # Widgets
        self._cb_raster_mode = QComboBox()
        self._cb_raster_mode.addItems([None] + list(_RASTER_MODES))

        # Layouts
        layout = _AcquisitionWidget._init_ui(self)
        layout.addRow('Raster mode', self._cb_raster_mode)

        # Singals
        self._cb_raster_mode.currentIndexChanged.connect(self.edited)

        return layout

    def parameter(self, parameter=None):
        parameter = _AcquisitionWidget.parameter(self, parameter)
        parameter.raster_mode = self._cb_raster_mode.currentText()
        return parameter

    def setParameter(self, condition):
        _AcquisitionWidget.setParameter(self, condition)
        self._cb_raster_mode.setCurrentIndex(self._cb_raster_mode.findText(condition.raster_mode))

    def setReadOnly(self, state):
        _AcquisitionWidget.setReadOnly(self, state)
        self._cb_raster_mode.setEnabled(not state)

    def isReadOnly(self):
        return _AcquisitionWidget.isReadOnly(self) and \
            not self._cb_raster_mode.isEnabled()

class AcquisitionRasterLinescanWidget(_AcquisitionRasterWidget):

    def __init__(self, parent=None):
        _AcquisitionRasterWidget.__init__(self, AcquisitionRasterLinescan, parent)

    def _init_ui(self):
        # Widgets
        self._txt_step_count = NumericalAttributeLineEdit(self.CLASS.step_count)
        self._txt_step_count.setFormat('{0:d}')
        self._txt_step_size = NumericalAttributeLineEdit(self.CLASS.step_size)
        self._txt_frame_count = NumericalAttributeLineEdit(self.CLASS.frame_count)
        self._txt_frame_count.setFormat('{0:d}')
        self._wdg_position_start = SpecimenPositionWidget(inline=True)
        self._wdg_position_end = SpecimenPositionWidget(inline=True)

        # Layout
        layout = _AcquisitionRasterWidget._init_ui(self)
        layout.insertRow(0, '<i>Step count</i>', self._txt_step_count)
        layout.insertRow(1, 'Step size', self._txt_step_size)
        layout.addRow('Frame count', self._txt_frame_count)
        layout.addRow('Start position', self._wdg_position_start)
        layout.addRow('End position', self._wdg_position_end)

        # Signals
        self._txt_step_count.textEdited.connect(self.edited)
        self._txt_step_size.textEdited.connect(self.edited)
        self._txt_frame_count.textEdited.connect(self.edited)
        self._wdg_position_start.edited.connect(self.edited)
        self._wdg_position_end.edited.connect(self.edited)

        return layout

    def _create_parameter(self):
        return self.CLASS(1)

    def parameter(self, parameter=None):
        parameter = _AcquisitionRasterWidget.parameter(self, parameter)
        parameter.step_count = self._txt_step_count.text()
        parameter.step_size = self._txt_step_size.text()
        parameter.frame_count = self._txt_frame_count.text()
        parameter.position_start = self._wdg_position_start.condition()
        parameter.position_end = self._wdg_position_end.condition()
        return parameter

    def setParameter(self, condition):
        _AcquisitionRasterWidget.setParameter(self, condition)
        self._txt_step_count.setText(condition.step_count)
        self._txt_step_size.setText(condition.step_size)
        self._txt_frame_count.setText(condition.frame_count)
        self._wdg_position_start.setParameter(condition.position_start)
        self._wdg_position_end.setParameter(condition.position_end)

    def setReadOnly(self, state):
        _AcquisitionRasterWidget.setReadOnly(self, state)
        self._txt_step_count.setReadOnly(state)
        self._txt_step_size.setReadOnly(state)
        self._txt_frame_count.setReadOnly(state)
        self._wdg_position_start.setReadOnly(state)
        self._wdg_position_end.setReadOnly(state)

    def isReadOnly(self):
        return _AcquisitionRasterWidget.isReadOnly(self) and \
            self._txt_step_count.isReadOnly() and \
            self._txt_step_size.isReadOnly() and \
            self._txt_frame_count.isReadOnly() and \
            self._wdg_position_start.isReadOnly() and \
            self._wdg_position_end.isReadOnly()

    def hasAcceptableInput(self):
        return _AcquisitionRasterWidget.hasAcceptableInput(self) and \
            self._txt_step_count.hasAcceptableInput() and \
            self._txt_step_size.hasAcceptableInput() and \
            self._txt_frame_count.hasAcceptableInput() and \
            self._wdg_position_start.hasAcceptableInput() and \
            self._wdg_position_end.hasAcceptableInput()

class AcquisitionRasterXYWidget(_AcquisitionRasterWidget):

    def __init__(self, parent=None):
        _AcquisitionRasterWidget.__init__(self, AcquisitionRasterXY, parent)

    def _init_ui(self):
        # Widgets
        self._txt_step_count_x = NumericalAttributeLineEdit(self.CLASS.step_count_x)
        self._txt_step_count_x.setFormat('{0:d}')
        self._txt_step_count_y = NumericalAttributeLineEdit(self.CLASS.step_count_y)
        self._txt_step_count_y.setFormat('{0:d}')
        self._txt_step_size_x = NumericalAttributeLineEdit(self.CLASS.step_size_x)
        self._txt_step_size_y = NumericalAttributeLineEdit(self.CLASS.step_size_y)
        self._txt_frame_count = NumericalAttributeLineEdit(self.CLASS.frame_count)
        self._txt_frame_count.setFormat('{0:d}')
        self._cb_location = QComboBox()
        self._cb_location.addItems(list(_POSITION_LOCATIONS))
        self._wdg_position = SpecimenPositionWidget(inline=True)

        # Layouts
        layout = _AcquisitionRasterWidget._init_ui(self)
        layout.insertRow(0, '<i>Step count (x)</i>', self._txt_step_count_x)
        layout.insertRow(1, '<i>Step count (y)</i>', self._txt_step_count_y)
        layout.insertRow(2, 'Step size (x)', self._txt_step_size_x)
        layout.insertRow(3, 'Step size (y)', self._txt_step_size_y)
        layout.addRow('Frame count', self._txt_frame_count)
        layout.addRow('Position', self._cb_location)
        layout.addWidget(self._wdg_position)

        # Signals
        self._txt_step_count_x.textEdited.connect(self.edited)
        self._txt_step_count_y.textEdited.connect(self.edited)
        self._txt_step_size_x.textEdited.connect(self.edited)
        self._txt_step_size_y.textEdited.connect(self.edited)
        self._txt_frame_count.textEdited.connect(self.edited)
        self._cb_location.currentIndexChanged.connect(self.edited)
        self._wdg_position.edited.connect(self.edited)

        return layout

    def _create_parameter(self):
        return self.CLASS(1, 1)

    def parameter(self, parameter=None):
        parameter = _AcquisitionRasterWidget.parameter(self, parameter)
        parameter.step_count_x = self._txt_step_count_x.text()
        parameter.step_count_y = self._txt_step_count_y.text()
        parameter.step_size_x = self._txt_step_size_x.text()
        parameter.step_size_y = self._txt_step_size_y.text()
        parameter.frame_count = self._txt_frame_count.text()
        parameter.position = (self._wdg_position.condition(),
                              self._cb_location.currentText())
        return parameter

    def setParameter(self, condition):
        _AcquisitionRasterWidget.setParameter(self, condition)
        self._txt_step_count_x.setText(condition.step_count_x)
        self._txt_step_count_y.setText(condition.step_count_y)
        self._txt_step_size_x.setText(condition.step_size_x)
        self._txt_step_size_y.setText(condition.step_size_y)
        self._txt_frame_count.setText(condition.frame_count)

        position, location = condition.get_position(True)
        self._cb_location.setCurrentIndex(self._cb_location.findText(location))
        if position is not None:
            self._wdg_position.setParameter(position)

    def setReadOnly(self, state):
        _AcquisitionRasterWidget.setReadOnly(self, state)
        self._txt_step_count_x.setReadOnly(state)
        self._txt_step_count_y.setReadOnly(state)
        self._txt_step_size_x.setReadOnly(state)
        self._txt_step_size_y.setReadOnly(state)
        self._txt_frame_count.setReadOnly(state)
        self._cb_location.setEnabled(not state)
        self._wdg_position.setReadOnly(state)

    def isReadOnly(self):
        return _AcquisitionRasterWidget.isReadOnly(self) and \
            self._txt_step_count_x.isReadOnly() and \
            self._txt_step_count_y.isReadOnly() and \
            self._txt_step_size_x.isReadOnly() and \
            self._txt_step_size_y.isReadOnly() and \
            self._txt_frame_count.isReadOnly() and \
            not self._cb_location.isEnabled() and \
            self._wdg_position.isReadOnly()

    def hasAcceptableInput(self):
        return _AcquisitionRasterWidget.hasAcceptableInput(self) and \
            self._txt_step_count_x.hasAcceptableInput() and \
            self._txt_step_count_y.hasAcceptableInput() and \
            self._txt_step_size_x.hasAcceptableInput() and \
            self._txt_step_size_y.hasAcceptableInput() and \
            self._txt_frame_count.hasAcceptableInput() and \
            self._wdg_position.hasAcceptableInput()

class AcquisitionRasterXYZWidget(_AcquisitionRasterWidget):

    def __init__(self, parent=None):
        _AcquisitionRasterWidget.__init__(self, AcquisitionRasterXYZ, parent)

    def _init_ui(self):
        # Widgets
        self._txt_step_count_x = NumericalAttributeLineEdit(self.CLASS.step_count_x)
        self._txt_step_count_x.setFormat('{0:d}')
        self._txt_step_count_y = NumericalAttributeLineEdit(self.CLASS.step_count_y)
        self._txt_step_count_y.setFormat('{0:d}')
        self._txt_step_count_z = NumericalAttributeLineEdit(self.CLASS.step_count_z)
        self._txt_step_count_z.setFormat('{0:d}')
        self._txt_step_size_x = NumericalAttributeLineEdit(self.CLASS.step_size_x)
        self._txt_step_size_y = NumericalAttributeLineEdit(self.CLASS.step_size_y)
        self._txt_step_size_z = NumericalAttributeLineEdit(self.CLASS.step_size_z)
        self._cb_raster_mode_z = QComboBox()
        self._cb_raster_mode_z.addItems([None] + list(_RASTER_MODES_Z))
        self._cb_location = QComboBox()
        self._cb_location.addItems(list(_POSITION_LOCATIONS))
        self._wdg_position = SpecimenPositionWidget(inline=True)

        # Layouts
        layout = _AcquisitionRasterWidget._init_ui(self)
        layout.insertRow(0, '<i>Step count (x)</i>', self._txt_step_count_x)
        layout.insertRow(1, '<i>Step count (y)</i>', self._txt_step_count_y)
        layout.insertRow(2, '<i>Step count (z)</i>', self._txt_step_count_z)
        layout.insertRow(3, 'Step size (x)', self._txt_step_size_x)
        layout.insertRow(4, 'Step size (y)', self._txt_step_size_y)
        layout.insertRow(5, 'Step size (z)', self._txt_step_size_z)
        layout.addRow('Raster mode (z)', self._cb_raster_mode_z)
        layout.addRow('Position', self._cb_location)
        layout.addWidget(self._wdg_position)

        # Signals
        self._txt_step_count_x.textEdited.connect(self.edited)
        self._txt_step_count_y.textEdited.connect(self.edited)
        self._txt_step_count_z.textEdited.connect(self.edited)
        self._txt_step_size_x.textEdited.connect(self.edited)
        self._txt_step_size_y.textEdited.connect(self.edited)
        self._txt_step_size_z.textEdited.connect(self.edited)
        self._cb_raster_mode_z.currentIndexChanged.connect(self.edited)
        self._cb_location.currentIndexChanged.connect(self.edited)
        self._wdg_position.edited.connect(self.edited)

        return layout

    def _create_parameter(self):
        return self.CLASS(1, 1, 1)

    def parameter(self, parameter=None):
        parameter = _AcquisitionRasterWidget.parameter(self, parameter)
        parameter.step_count_x = self._txt_step_count_x.text()
        parameter.step_count_y = self._txt_step_count_y.text()
        parameter.step_count_z = self._txt_step_count_z.text()
        parameter.step_size_x = self._txt_step_size_x.text()
        parameter.step_size_y = self._txt_step_size_y.text()
        parameter.step_size_z = self._txt_step_size_z.text()
        parameter.raster_mode_z = self._cb_raster_mode_z.currentText()
        parameter.position = (self._wdg_position.condition(),
                              self._cb_location.currentText())
        return parameter

    def setParameter(self, condition):
        _AcquisitionRasterWidget.setParameter(self, condition)
        self._txt_step_count_x.setText(condition.step_count_x)
        self._txt_step_count_y.setText(condition.step_count_y)
        self._txt_step_count_z.setText(condition.step_count_z)
        self._txt_step_size_x.setText(condition.step_size_x)
        self._txt_step_size_y.setText(condition.step_size_y)
        self._txt_step_size_z.setText(condition.step_size_z)
        self._cb_raster_mode_z.setCurrentIndex(self._cb_raster_mode_z.findText(condition.raster_mode_z))

        position, location = condition.get_position(True)
        self._cb_location.setCurrentIndex(self._cb_location.findText(location))
        if position is not None:
            self._wdg_position.setParameter(position)

    def setReadOnly(self, state):
        _AcquisitionRasterWidget.setReadOnly(self, state)
        self._txt_step_count_x.setReadOnly(state)
        self._txt_step_count_y.setReadOnly(state)
        self._txt_step_count_z.setReadOnly(state)
        self._txt_step_size_x.setReadOnly(state)
        self._txt_step_size_y.setReadOnly(state)
        self._txt_step_size_z.setReadOnly(state)
        self._cb_raster_mode_z.setEnabled(not state)
        self._cb_location.setEnabled(not state)
        self._wdg_position.setReadOnly(state)

    def isReadOnly(self):
        return _AcquisitionRasterWidget.isReadOnly(self) and \
            self._txt_step_count_x.isReadOnly() and \
            self._txt_step_count_y.isReadOnly() and \
            self._txt_step_count_z.isReadOnly() and \
            self._txt_step_size_x.isReadOnly() and \
            self._txt_step_size_y.isReadOnly() and \
            self._txt_step_size_z.isReadOnly() and \
            not self._cb_raster_mode_z.isEnabled() and \
            not self._cb_location.isEnabled() and \
            self._wdg_position.isReadOnly()

    def hasAcceptableInput(self):
        return _AcquisitionRasterWidget.hasAcceptableInput(self) and \
            self._txt_step_count_x.hasAcceptableInput() and \
            self._txt_step_count_y.hasAcceptableInput() and \
            self._txt_step_count_z.hasAcceptableInput() and \
            self._txt_step_size_x.hasAcceptableInput() and \
            self._txt_step_size_y.hasAcceptableInput() and \
            self._txt_step_size_z.hasAcceptableInput() and \
            self._wdg_position.hasAcceptableInput()

