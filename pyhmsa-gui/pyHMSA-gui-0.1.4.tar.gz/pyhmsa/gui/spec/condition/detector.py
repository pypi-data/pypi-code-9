"""
Detector widgets
"""

# Standard library modules.
from operator import methodcaller

# Third party modules.
from PySide.QtGui import \
    QComboBox, QToolBar, QMessageBox, QTableView, QItemDelegate
from PySide.QtCore import Qt, QAbstractTableModel, QModelIndex

# Local modules.
from pyhmsa.gui.util.parameter import \
    (ParameterWidget, NumericalAttributeLineEdit,
     TextAttributeLineEdit, UnitAttributeLineEdit)
from pyhmsa.gui.util.icon import getIcon
from pyhmsa.gui.spec.condition.condition import _ConditionWidget
from pyhmsa.gui.spec.condition.calibration import CalibrationWidget

from pyhmsa.spec.condition.detector import \
    (PulseHeightAnalyser, Window, WindowLayer,
     DetectorCamera, DetectorSpectrometer, DetectorSpectrometerCL,
     DetectorSpectrometerWDS, DetectorSpectrometerXEDS)
from pyhmsa.spec.condition.calibration import CalibrationConstant

# Globals and constants variables.
from pyhmsa.spec.condition.detector import \
    _SIGNAL_TYPES, _COLLECTION_MODES, _PHA_MODES, _XEDS_TECHNOLOGIES

class PulseHeightAnalyserWidget(ParameterWidget):

    def __init__(self, parent=None):
        ParameterWidget.__init__(self, PulseHeightAnalyser, parent)

    def _init_ui(self):
        # Widgets
        self._txt_bias = NumericalAttributeLineEdit(self.CLASS.bias)
        self._txt_gain = NumericalAttributeLineEdit(self.CLASS.gain)
        self._txt_base_level = NumericalAttributeLineEdit(self.CLASS.base_level)
        self._txt_window = NumericalAttributeLineEdit(self.CLASS.window)
        self._cb_mode = QComboBox()
        self._cb_mode.addItems([None] + list(_PHA_MODES))

        # Layouts
        layout = ParameterWidget._init_ui(self)
        layout.addRow('Bias', self._txt_bias)
        layout.addRow('Gain', self._txt_gain)
        layout.addRow('Base level', self._txt_base_level)
        layout.addRow('Window', self._txt_window)
        layout.addRow('Mode', self._cb_mode)

        # Signals
        self._txt_bias.textEdited.connect(self.edited)
        self._txt_gain.textEdited.connect(self.edited)
        self._txt_base_level.textEdited.connect(self.edited)
        self._txt_window.textEdited.connect(self.edited)
        self._cb_mode.currentIndexChanged.connect(self.edited)

        return layout

    def parameter(self, parameter=None):
        parameter = ParameterWidget.parameter(self, parameter)
        parameter.bias = self._txt_bias.text()
        parameter.gain = self._txt_gain.text()
        parameter.base_level = self._txt_base_level.text()
        parameter.window = self._txt_window.text()
        parameter.mode = self._cb_mode.currentText()
        return parameter

    def setParameter(self, parameter):
        ParameterWidget.setParameter(self, parameter)
        self._txt_bias.setText(parameter.bias)
        self._txt_gain.setText(parameter.gain)
        self._txt_base_level.setText(parameter.base_level)
        self._txt_window.setText(parameter.window)
        self._cb_mode.setCurrentIndex(self._cb_mode.findText(parameter.mode))

    def pulseHeightAnalyser(self):
        return self.parameter()

    def setPulseHeightAnalyser(self, pha):
        self.setParameter(pha)

    pha = pulseHeightAnalyser

    setPha = setPulseHeightAnalyser

    def setReadOnly(self, state):
        ParameterWidget.setReadOnly(self, state)
        self._txt_bias.setReadOnly(state)
        self._txt_gain.setReadOnly(state)
        self._txt_base_level.setReadOnly(state)
        self._txt_window.setReadOnly(state)
        self._cb_mode.setEnabled(not state)

    def isReadOnly(self):
        return ParameterWidget.isReadOnly(self) and \
            self._txt_bias.isReadOnly() and \
            self._txt_gain.isReadOnly() and \
            self._txt_base_level.isReadOnly() and \
            self._txt_window.isReadOnly() and \
            not self._cb_mode.isEnabled()

    def hasAcceptableInput(self):
        return ParameterWidget.hasAcceptableInput(self) and \
            self._txt_bias.hasAcceptableInput() and \
            self._txt_gain.hasAcceptableInput() and \
            self._txt_base_level.hasAcceptableInput() and \
            self._txt_window.hasAcceptableInput()

class WindowWidget(ParameterWidget):

    class _WindowModel(QAbstractTableModel):

        def __init__(self):
            QAbstractTableModel.__init__(self)
            self.layers = []

        def rowCount(self, *args, **kwargs):
            return len(self.layers)

        def columnCount(self, *args, **kwargs):
            return 2

        def data(self, index, role):
            if not index.isValid() or not (0 <= index.row() < len(self.layers)):
                return None
            if role != Qt.DisplayRole:
                return None

            layer = self.layers[index.row()]
            column = index.column()
            if column == 0:
                return layer.material
            elif column == 1:
                return '%s' % layer.thickness

        def headerData(self, section , orientation, role):
            if role != Qt.DisplayRole:
                return None
            if orientation == Qt.Horizontal:
                if section == 0:
                    return 'Material'
                elif section == 1:
                    return 'Thickness'
            elif orientation == Qt.Vertical:
                return str(section + 1)

        def flags(self, index):
            if not index.isValid():
                return Qt.ItemIsEnabled

            return Qt.ItemFlags(QAbstractTableModel.flags(self, index) |
                                Qt.ItemIsEditable)

        def setData(self, index, value, role=Qt.EditRole):
            if not index.isValid() or \
                    not (0 <= index.row() < len(self.layers)):
                return False

            layer = self.layers[index.row()]
            column = index.column()
            if column == 0:
                layer.material = value
            elif column == 1:
                layer.thickness = value

            self.dataChanged.emit(index, index)
            return True

        def insertRows(self, row, count=1, parent=None):
            if count == 0:
                return False
            if parent is None:
                parent = QModelIndex()
            self.beginInsertRows(parent, row, row + count - 1)

            for i in range(count):
                self.layers.insert(row + i, WindowLayer("unknown", 0.0))

            self.endInsertRows()
            return True

        def removeRows(self, row, count=1, parent=None):
            if count == 0:
                return False
            if parent is None:
                parent = QModelIndex()
            self.beginRemoveRows(parent, row, row + count - 1)

            self.layers = self.layers[:row] + self.layers[row + count:]

            self.endRemoveRows()
            return True

    class _WindowDelegate(QItemDelegate):

        def __init__(self, parent=None):
            QItemDelegate.__init__(self, parent)

        def createEditor(self, parent, option, index):
            column = index.column()
            if column == 0:
                return TextAttributeLineEdit(WindowLayer.material, parent)
            elif column == 1:
                return NumericalAttributeLineEdit(WindowLayer.thickness, parent)
            else:
                return QItemDelegate.createEditor(self, parent, option, index)

        def setEditorData(self, editor, index):
            text = index.model().data(index, Qt.DisplayRole)
            column = index.column()
            if column == 0:
                editor.setText(text)
            elif column == 1:
                editor.setText(text)
            else:
                QItemDelegate.setEditorData(self, editor, index)

        def setModelData(self, editor, model, index):
            column = index.column()
            if column == 0:
                model.setData(index, editor.text())
            elif column == 1:
                model.setData(index, editor.text())
            else:
                return QItemDelegate.setModelData(self, editor, model, index)

    def __init__(self, parent=None):
        ParameterWidget.__init__(self, Window, parent)

    def _init_ui(self):
        # Widgets
        model = self._WindowModel()

        self._table = QTableView()
        self._table.setModel(model)
        self._table.setItemDelegate(self._WindowDelegate(self))
        self._table.horizontalHeader().setStretchLastSection(True)

        self._toolbar = QToolBar()
        action_add = self._toolbar.addAction(getIcon("list-add"), "Add layer")
        action_remove = self._toolbar.addAction(getIcon("list-remove"), "Remove layer")

        # Layouts
        layout = ParameterWidget._init_ui(self)
        layout.addRow(self._table)
        layout.addRow(self._toolbar)

        # Signals
        action_add.triggered.connect(self._on_add)
        action_remove.triggered.connect(self._on_remove)

        model.dataChanged.connect(self.edited)
        model.rowsInserted.connect(self.edited)
        model.rowsRemoved.connect(self.edited)

        return layout

    def _on_add(self):
        index = self._table.selectionModel().currentIndex()
        model = self._table.model()
        model.insertRows(index.row() + 1)

    def _on_remove(self):
        selection = self._table.selectionModel().selection().indexes()
        if len(selection) == 0:
            QMessageBox.warning(self, "Window layer", "Select a layer")
            return

        model = self._table.model()
        for row in sorted(map(methodcaller('row'), selection), reverse=True):
            model.removeRow(row)

    def parameter(self, parameter=None):
        parameter = ParameterWidget.parameter(self, parameter)
        parameter.layers.clear()
        for layer in self._table.model().layers:
            parameter.append_layer(layer.material, layer.thickness) # copy
        return parameter

    def setParameter(self, window):
        model = self._table.model()
        model.layers = window.layers
        model.reset()

    def window(self):
        return self.parameter()

    def setWindow(self, window):
        self.setParameter(window)

    def setReadOnly(self, state):
        ParameterWidget.setReadOnly(self, state)
        if state:
            trigger = QTableView.EditTrigger.NoEditTriggers
        else:
            trigger = QTableView.EditTrigger.AllEditTriggers
        self._table.setEditTriggers(trigger)
        self._toolbar.setEnabled(not state)

    def isReadOnly(self):
        return ParameterWidget.isReadOnly(self) and \
            self._table.editTriggers() == QTableView.EditTrigger.NoEditTriggers and \
            not self._toolbar.isEnabled()

class _DetectorWidget(_ConditionWidget):

    def _init_ui(self):
        # Widgets
        self._cb_signal_type = QComboBox()
        self._cb_signal_type.addItems([None] + list(_SIGNAL_TYPES))
        self._txt_manufacturer = TextAttributeLineEdit(self.CLASS.manufacturer)
        self._txt_model = TextAttributeLineEdit(self.CLASS.model)
        self._txt_serial_number = TextAttributeLineEdit(self.CLASS.serial_number)
        self._txt_measurement_unit = UnitAttributeLineEdit(self.CLASS.measurement_unit)
        self._txt_elevation = NumericalAttributeLineEdit(self.CLASS.elevation)
        self._txt_azimuth = NumericalAttributeLineEdit(self.CLASS.azimuth)
        self._txt_distance = NumericalAttributeLineEdit(self.CLASS.distance)
        self._txt_area = NumericalAttributeLineEdit(self.CLASS.area)
        self._txt_solid_angle = NumericalAttributeLineEdit(self.CLASS.solid_angle)
        self._txt_semi_angle = NumericalAttributeLineEdit(self.CLASS.semi_angle)
        self._txt_temperature = NumericalAttributeLineEdit(self.CLASS.temperature)

        # Layout
        layout = _ConditionWidget._init_ui(self)
        layout.addRow('Type of signal', self._cb_signal_type)
        layout.addRow('Manufacturer', self._txt_manufacturer)
        layout.addRow('Model', self._txt_model)
        layout.addRow('Serial number', self._txt_serial_number)
        layout.addRow('Measurement unit', self._txt_measurement_unit)
        layout.addRow('Elevation', self._txt_elevation)
        layout.addRow('Azimuth', self._txt_azimuth)
        layout.addRow('Distance', self._txt_distance)
        layout.addRow('Area', self._txt_area)
        layout.addRow('Solid angle', self._txt_solid_angle)
        layout.addRow('Semi angle', self._txt_semi_angle)
        layout.addRow('Temperature', self._txt_temperature)

        # Signals
        self._cb_signal_type.currentIndexChanged.connect(self.edited)
        self._txt_manufacturer.textEdited.connect(self.edited)
        self._txt_model.textEdited.connect(self.edited)
        self._txt_serial_number.textEdited.connect(self.edited)
        self._txt_measurement_unit.textEdited.connect(self.edited)
        self._txt_elevation.textEdited.connect(self.edited)
        self._txt_azimuth.textEdited.connect(self.edited)
        self._txt_distance.textEdited.connect(self.edited)
        self._txt_area.textEdited.connect(self.edited)
        self._txt_solid_angle.textEdited.connect(self.edited)
        self._txt_semi_angle.textEdited.connect(self.edited)
        self._txt_temperature.textEdited.connect(self.edited)

        return layout

    def parameter(self, parameter=None):
        parameter = _ConditionWidget.parameter(self, parameter)
        parameter.signal_type = self._cb_signal_type.currentText()
        parameter.manufacturer = self._txt_manufacturer.text()
        parameter.model = self._txt_model.text()
        parameter.serial_number = self._txt_serial_number.text()
        parameter.measurement_unit = self._txt_measurement_unit.text()
        parameter.elevation = self._txt_elevation.text()
        parameter.azimuth = self._txt_azimuth.text()
        parameter.distance = self._txt_distance.text()
        parameter.area = self._txt_area.text()
        parameter.solid_angle = self._txt_solid_angle.text()
        parameter.semi_angle = self._txt_semi_angle.text()
        parameter.temperature = self._txt_temperature.text()
        return parameter

    def setParameter(self, condition):
        _ConditionWidget.setParameter(self, condition)
        self._cb_signal_type.setCurrentIndex(self._cb_signal_type.findText(condition.signal_type))
        self._txt_manufacturer.setText(condition.manufacturer)
        self._txt_model.setText(condition.model)
        self._txt_serial_number.setText(condition.serial_number)
        self._txt_measurement_unit.setText(condition.measurement_unit)
        self._txt_elevation.setText(condition.elevation)
        self._txt_azimuth.setText(condition.azimuth)
        self._txt_distance.setText(condition.distance)
        self._txt_area.setText(condition.area)
        self._txt_solid_angle.setText(condition.solid_angle)
        self._txt_semi_angle.setText(condition.semi_angle)
        self._txt_temperature.setText(condition.temperature)

    def setReadOnly(self, state):
        _ConditionWidget.setReadOnly(self, state)
        self._cb_signal_type.setEnabled(not state)
        self._txt_manufacturer.setReadOnly(state)
        self._txt_model.setReadOnly(state)
        self._txt_serial_number.setReadOnly(state)
        self._txt_measurement_unit.setReadOnly(state)
        self._txt_elevation.setReadOnly(state)
        self._txt_azimuth.setReadOnly(state)
        self._txt_distance.setReadOnly(state)
        self._txt_area.setReadOnly(state)
        self._txt_solid_angle.setReadOnly(state)
        self._txt_semi_angle.setReadOnly(state)
        self._txt_temperature.setReadOnly(state)

    def isReadOnly(self):
        return _ConditionWidget.isReadOnly(self) and \
            not self._cb_signal_type.isEnabled() and \
            self._txt_manufacturer.isReadOnly() and \
            self._txt_model.isReadOnly() and \
            self._txt_serial_number.isReadOnly() and \
            self._txt_measurement_unit.isReadOnly() and \
            self._txt_elevation.isReadOnly() and \
            self._txt_azimuth.isReadOnly() and \
            self._txt_distance.isReadOnly() and \
            self._txt_area.isReadOnly() and \
            self._txt_solid_angle.isReadOnly() and \
            self._txt_semi_angle.isReadOnly() and \
            self._txt_temperature.isReadOnly()

    def hasAcceptableInput(self):
        return _ConditionWidget.hasAcceptableInput(self) and \
            self._txt_manufacturer.hasAcceptableInput() and \
            self._txt_model.hasAcceptableInput() and \
            self._txt_serial_number.hasAcceptableInput() and \
            self._txt_measurement_unit.hasAcceptableInput() and \
            self._txt_elevation.hasAcceptableInput() and \
            self._txt_azimuth.hasAcceptableInput() and \
            self._txt_distance.hasAcceptableInput() and \
            self._txt_area.hasAcceptableInput() and \
            self._txt_solid_angle.hasAcceptableInput() and \
            self._txt_semi_angle.hasAcceptableInput() and \
            self._txt_temperature.hasAcceptableInput()

class DetectorCameraWidget(_DetectorWidget):

    def __init__(self, parent=None):
        _DetectorWidget.__init__(self, DetectorCamera, parent)

    def _init_ui(self):
        # Widgets
        self._txt_pixel_count_u = NumericalAttributeLineEdit(self.CLASS.pixel_count_u)
        self._txt_pixel_count_u.setFormat('{0:d}')
        self._txt_pixel_count_v = NumericalAttributeLineEdit(self.CLASS.pixel_count_v)
        self._txt_pixel_count_v.setFormat('{0:d}')
        self._txt_exposure_time = NumericalAttributeLineEdit(self.CLASS.exposure_time)
        self._txt_magnification = NumericalAttributeLineEdit(self.CLASS.magnification)
        self._txt_magnification.setFormat('{0:d}')
        self._txt_focal_length = NumericalAttributeLineEdit(self.CLASS.focal_length)

        # Layout
        layout = _DetectorWidget._init_ui(self)
        layout.insertRow(0, 'Horizontal pixel count', self._txt_pixel_count_u)
        layout.insertRow(1, 'Vertical pixel count', self._txt_pixel_count_v)
        layout.addRow('Exposure time', self._txt_exposure_time)
        layout.addRow('Magnification', self._txt_magnification)
        layout.addRow('Focal length', self._txt_focal_length)

        # Signals
        self._txt_pixel_count_u.textEdited.connect(self.edited)
        self._txt_pixel_count_v.textEdited.connect(self.edited)
        self._txt_exposure_time.textEdited.connect(self.edited)
        self._txt_magnification.textEdited.connect(self.edited)
        self._txt_focal_length.textEdited.connect(self.edited)

        return layout

    def _create_parameter(self):
        return self.CLASS(1, 1)

    def parameter(self, parameter=None):
        parameter = _DetectorWidget.parameter(self, parameter)
        parameter.pixel_count_u = self._txt_pixel_count_u.text()
        parameter.pixel_count_v = self._txt_pixel_count_v.text()
        parameter.exposure_time = self._txt_exposure_time.text()
        parameter.magnification = self._txt_magnification.text()
        parameter.focal_length = self._txt_focal_length.text()
        return parameter

    def setParameter(self, condition):
        _DetectorWidget.setParameter(self, condition)
        self._txt_pixel_count_u.setText(condition.pixel_count_u)
        self._txt_pixel_count_v.setText(condition.pixel_count_v)
        self._txt_exposure_time.setText(condition.exposure_time)
        self._txt_magnification.setText(condition.magnification)
        self._txt_focal_length.setText(condition.focal_length)

    def setReadOnly(self, state):
        _DetectorWidget.setReadOnly(self, state)
        self._txt_pixel_count_u.setReadOnly(state)
        self._txt_pixel_count_v.setReadOnly(state)
        self._txt_exposure_time.setReadOnly(state)
        self._txt_magnification.setReadOnly(state)
        self._txt_focal_length.setReadOnly(state)

    def isReadOnly(self):
        return _DetectorWidget.isReadOnly(self) and \
            self._txt_pixel_count_u.isReadOnly() and \
            self._txt_pixel_count_v.isReadOnly() and \
            self._txt_exposure_time.isReadOnly() and \
            self._txt_magnification.isReadOnly() and \
            self._txt_focal_length.isReadOnly()

    def hasAcceptableInput(self):
        return _DetectorWidget.hasAcceptableInput(self) and \
            self._txt_pixel_count_u.hasAcceptableInput() and \
            self._txt_pixel_count_v.hasAcceptableInput() and \
            self._txt_exposure_time.hasAcceptableInput() and \
            self._txt_magnification.hasAcceptableInput() and \
            self._txt_focal_length.hasAcceptableInput()

class DetectorSpectrometerWidget(_DetectorWidget):

    def __init__(self, parent=None):
        _DetectorWidget.__init__(self, DetectorSpectrometer, parent)

    def _init_ui(self):
        # Widgets
        self._txt_channel_count = NumericalAttributeLineEdit(self.CLASS.channel_count)
        self._txt_channel_count.setFormat('{0:d}')
        self._wdg_calibration = CalibrationWidget()
        self._cb_collection_mode = QComboBox()
        self._cb_collection_mode.addItems([None] + list(_COLLECTION_MODES))

        # Layout
        layout = _DetectorWidget._init_ui(self)
        layout.insertRow(0, '<i>Channel count</i>', self._txt_channel_count)
        layout.insertRow(1, '<i>Calibration</i>', self._wdg_calibration)
        layout.addRow('Collection mode', self._cb_collection_mode)

        # Signals
        self._txt_channel_count.textEdited.connect(self.edited)
        self._wdg_calibration.edited.connect(self.edited)
        self._cb_collection_mode.currentIndexChanged.connect(self.edited)

        return layout

    def _create_parameter(self):
        return self.CLASS(1, CalibrationConstant('Quantity', 'm', 0.0))

    def parameter(self, parameter=None):
        parameter = _DetectorWidget.parameter(self, parameter)
        parameter.channel_count = self._txt_channel_count.text()
        parameter.calibration = self._wdg_calibration.calibration()
        parameter.collection_mode = self._cb_collection_mode.currentText()
        return parameter

    def setParameter(self, condition):
        _DetectorWidget.setParameter(self, condition)
        self._txt_channel_count.setText(condition.channel_count)
        self._wdg_calibration.setCalibration(condition.calibration)
        self._cb_collection_mode.setCurrentIndex(self._cb_collection_mode.findText(condition.collection_mode))

    def setReadOnly(self, state):
        _DetectorWidget.setReadOnly(self, state)
        self._txt_channel_count.setReadOnly(state)
        self._wdg_calibration.setReadOnly(state)
        self._cb_collection_mode.setEnabled(not state)

    def isReadOnly(self):
        return _DetectorWidget.isReadOnly(self) and \
            self._txt_channel_count.isReadOnly() and \
            self._wdg_calibration.isReadOnly() and \
            not self._cb_collection_mode.isEnabled()

    def hasAcceptableInput(self):
        return _DetectorWidget.hasAcceptableInput(self) and \
            self._txt_channel_count.hasAcceptableInput() and \
            self._wdg_calibration.hasAcceptableInput()

class DetectorSpectrometerCLWidget(DetectorSpectrometerWidget):

    def __init__(self, parent=None):
        _DetectorWidget.__init__(self, DetectorSpectrometerCL, parent)

    def _init_ui(self):
        # Widgets
        self._txt_grating_d = NumericalAttributeLineEdit(self.CLASS.grating_d)

        # Layouts
        layout = DetectorSpectrometerWidget._init_ui(self)
        layout.addRow('Grating spacing', self._txt_grating_d)

        # Signals
        self._txt_grating_d.textEdited.connect(self.edited)

        return layout

    def _create_parameter(self):
        return self.CLASS(1, CalibrationConstant('Quantity', 'm', 0.0))

    def parameter(self, parameter=None):
        parameter = DetectorSpectrometerWidget.parameter(self, parameter)
        parameter.grating_d = self._txt_grating_d.text()
        return parameter

    def setParameter(self, condition):
        DetectorSpectrometerWidget.setParameter(self, condition)
        self._txt_grating_d.setText(condition.grating_d)

    def setReadOnly(self, state):
        DetectorSpectrometerWidget.setReadOnly(self, state)
        self._txt_grating_d.setReadOnly(state)

    def isReadOnly(self):
        return DetectorSpectrometerWidget.isReadOnly(self) and \
            self._txt_grating_d.isReadOnly()

    def hasAcceptableInput(self):
        return DetectorSpectrometerWidget.hasAcceptableInput(self) and \
            self._txt_grating_d.hasAcceptableInput()

class DetectorSpectrometerWDSWidget(DetectorSpectrometerWidget):

    def __init__(self, parent=None):
        _DetectorWidget.__init__(self, DetectorSpectrometerWDS, parent)

    def _init_ui(self):
        # Widgets
        self._txt_dispersion_element = TextAttributeLineEdit(self.CLASS.dispersion_element)
        self._txt_crystal_2d = NumericalAttributeLineEdit(self.CLASS.crystal_2d)
        self._txt_rowland_circle_diameter = NumericalAttributeLineEdit(self.CLASS.rowland_circle_diameter)
        self._wdg_pulse_height_analyser = PulseHeightAnalyserWidget()
        self._wdg_window = WindowWidget()

        # Layouts
        layout = DetectorSpectrometerWidget._init_ui(self)
        layout.addRow('Dispersion element', self._txt_dispersion_element)
        layout.addRow('Crystal 2d-spacing', self._txt_crystal_2d)
        layout.addRow('Rowland circle diameter', self._txt_rowland_circle_diameter)
        layout.addRow('Pulse height analyser', self._wdg_pulse_height_analyser)
        layout.addRow('Window', self._wdg_window)

        # Signals
        self._txt_dispersion_element.textEdited.connect(self.edited)
        self._txt_crystal_2d.textEdited.connect(self.edited)
        self._txt_rowland_circle_diameter.textEdited.connect(self.edited)
        self._wdg_pulse_height_analyser.edited.connect(self.edited)
        self._wdg_window.edited.connect(self.edited)

        return layout

    def _create_parameter(self):
        return self.CLASS(1, CalibrationConstant('Quantity', 'm', 0.0))

    def parameter(self, parameter=None):
        parameter = DetectorSpectrometerWidget.parameter(self, parameter)
        parameter.dispersion_element = self._txt_dispersion_element.text()
        parameter.crystal_2d = self._txt_crystal_2d.text()
        parameter.rowland_circle_diameter = self._txt_rowland_circle_diameter.text()
        parameter.pulse_height_analyser = self._wdg_pulse_height_analyser.pha()
        parameter.window = self._wdg_window.window()
        return parameter

    def setParameter(self, condition):
        DetectorSpectrometerWidget.setParameter(self, condition)
        self._txt_dispersion_element.setText(condition.dispersion_element)
        self._txt_crystal_2d.setText(condition.crystal_2d)
        self._txt_rowland_circle_diameter.setText(condition.rowland_circle_diameter)
        self._wdg_pulse_height_analyser.setPha(condition.pulse_height_analyser)
        self._wdg_window.setWindow(condition.window)

    def setReadOnly(self, state):
        DetectorSpectrometerWidget.setReadOnly(self, state)
        self._txt_dispersion_element.setReadOnly(state)
        self._txt_crystal_2d.setReadOnly(state)
        self._txt_rowland_circle_diameter.setReadOnly(state)
        self._wdg_pulse_height_analyser.setReadOnly(state)
        self._wdg_window.setReadOnly(state)

    def isReadOnly(self):
        return DetectorSpectrometerWidget.isReadOnly(self) and \
            self._txt_dispersion_element.isReadOnly() and \
            self._txt_crystal_2d.isReadOnly() and \
            self._txt_rowland_circle_diameter.isReadOnly() and \
            self._wdg_pulse_height_analyser.isReadOnly() and \
            self._wdg_window.isReadOnly()

    def hasAcceptableInput(self):
        return DetectorSpectrometerWidget.hasAcceptableInput(self) and \
            self._txt_dispersion_element.hasAcceptableInput() and \
            self._txt_crystal_2d.hasAcceptableInput() and \
            self._txt_rowland_circle_diameter.hasAcceptableInput() and \
            self._wdg_pulse_height_analyser.hasAcceptableInput() and \
            self._wdg_window.hasAcceptableInput()

class DetectorSpectrometerXEDSWidget(DetectorSpectrometerWidget):

    def __init__(self, parent=None):
        _DetectorWidget.__init__(self, DetectorSpectrometerXEDS, parent)

    def _init_ui(self):
        # Widgets
        self._cb_technology = QComboBox()
        self._cb_technology.addItems([None] + list(_XEDS_TECHNOLOGIES))
        self._txt_nominal_throughput = NumericalAttributeLineEdit(self.CLASS.nominal_throughput)
        self._txt_time_constant = NumericalAttributeLineEdit(self.CLASS.time_constant)
        self._txt_strobe_rate = NumericalAttributeLineEdit(self.CLASS.strobe_rate)
        self._wdg_window = WindowWidget()

        # Layout
        form = DetectorSpectrometerWidget._init_ui(self)
        form.addRow('Technology', self._cb_technology)
        form.addRow('Nominal throughput', self._txt_nominal_throughput)
        form.addRow('Time constant', self._txt_time_constant)
        form.addRow('Strobe rate', self._txt_strobe_rate)
        form.addRow('Window', self._wdg_window)

        # Signals
        self._cb_technology.currentIndexChanged.connect(self.edited)
        self._txt_nominal_throughput.textEdited.connect(self.edited)
        self._txt_time_constant.textEdited.connect(self.edited)
        self._txt_strobe_rate.textEdited.connect(self.edited)
        self._wdg_window.edited.connect(self.edited)

        return form

    def _create_parameter(self):
        return self.CLASS(1, CalibrationConstant('Quantity', 'm', 0.0))

    def parameter(self, parameter=None):
        parameter = DetectorSpectrometerWidget.parameter(self, parameter)
        parameter.technology = self._cb_technology.currentText()
        parameter.nominal_throughput = self._txt_nominal_throughput.text()
        parameter.time_constant = self._txt_time_constant.text()
        parameter.strobe_rate = self._txt_strobe_rate.text()
        parameter.window = self._wdg_window.window()
        return parameter

    def setParameter(self, condition):
        DetectorSpectrometerWidget.setParameter(self, condition)
        self._cb_technology.setCurrentIndex(self._cb_technology.findText(condition.technology))
        self._txt_nominal_throughput.setText(condition.nominal_throughput)
        self._txt_time_constant.setText(condition.time_constant)
        self._txt_strobe_rate.setText(condition.strobe_rate)
        self._wdg_window.setWindow(condition.window)

    def setReadOnly(self, state):
        DetectorSpectrometerWidget.setReadOnly(self, state)
        self._cb_technology.setEnabled(not state)
        self._txt_nominal_throughput.setReadOnly(state)
        self._txt_time_constant.setReadOnly(state)
        self._txt_strobe_rate.setReadOnly(state)
        self._wdg_window.setReadOnly(state)

    def isReadOnly(self):
        return DetectorSpectrometerWidget.isReadOnly(self) and \
            not self._cb_technology.isEnabled() and \
            self._txt_nominal_throughput.isReadOnly() and \
            self._txt_time_constant.isReadOnly() and \
            self._txt_strobe_rate.isReadOnly() and \
            self._wdg_window.isReadOnly()

    def hasAcceptableInput(self):
        return DetectorSpectrometerWidget.hasAcceptableInput(self) and \
            self._txt_nominal_throughput.hasAcceptableInput() and \
            self._txt_time_constant.hasAcceptableInput() and \
            self._txt_strobe_rate.hasAcceptableInput() and \
            self._wdg_window.hasAcceptableInput()
