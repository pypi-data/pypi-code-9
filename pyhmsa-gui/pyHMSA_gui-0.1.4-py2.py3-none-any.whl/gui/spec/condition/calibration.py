"""
Calibration widgets
"""

# Standard library modules.
import re

# Third party modules.
from PySide.QtGui import QValidator, QComboBox, QStackedWidget

from pkg_resources import iter_entry_points #@UnresolvedImport

# Local modules.
from pyhmsa.gui.util.parameter import \
    ParameterWidget, _AttributeLineEdit, TextAttributeLineEdit, UnitAttributeLineEdit, NumericalAttributeLineEdit

from pyhmsa.spec.condition.calibration import \
    (_Calibration, CalibrationConstant, CalibrationLinear,
     CalibrationPolynomial, CalibrationExplicit)

# Globals and constants variables.

class _CalibrationWidget(ParameterWidget):

    def _init_ui(self):
        # Widgets
        self._txt_quantity = TextAttributeLineEdit(self.CLASS.quantity)
        self._txt_unit = UnitAttributeLineEdit(self.CLASS.unit)

        # Layouts
        layout = ParameterWidget._init_ui(self)
        layout.addRow('<i>Quantity</i>', self._txt_quantity)
        layout.addRow('<i>Unit</i>', self._txt_unit)

        # Signals
        self._txt_quantity.textEdited.connect(self.edited)
        self._txt_unit.textEdited.connect(self.edited)

        return layout

    def parameter(self, parameter=None):
        parameter = ParameterWidget.parameter(self, parameter)
        parameter.quantity = self._txt_quantity.text()
        parameter.unit = self._txt_unit.text()
        return parameter

    def setParameter(self, calibration):
        self._txt_quantity.setText(calibration.quantity)
        self._txt_unit.setText(calibration.unit)

    def setReadOnly(self, state):
        ParameterWidget.setReadOnly(self, state)
        self._txt_quantity.setReadOnly(state)
        self._txt_unit.setReadOnly(state)

    def isReadOnly(self):
        return ParameterWidget.isReadOnly(self) and \
            self._txt_quantity.isReadOnly() and \
            self._txt_unit.isReadOnly()

    def hasAcceptableInput(self):
        return ParameterWidget.hasAcceptableInput(self) and \
            self._txt_quantity.hasAcceptableInput() and \
            self._txt_unit.hasAcceptableInput()

    def calibration(self):
        return self.parameter()

    def setCalibration(self, calibration):
        self.setParameter(calibration)

class CalibrationConstantWidget(_CalibrationWidget):

    def __init__(self, parent=None):
        _CalibrationWidget.__init__(self, CalibrationConstant, parent)
        self.setAccessibleName('constant')

    def _init_ui(self):
        # Widgets
        self._txt_value = NumericalAttributeLineEdit(self.CLASS.value)

        # Layouts
        layout = _CalibrationWidget._init_ui(self)
        layout.addRow('<i>Value</i>', self._txt_value)

        # Signals
        self._txt_value.textEdited.connect(self.edited)

        return layout

    def _create_parameter(self):
        return self.CLASS('Quantity', 'm', 0.0)

    def parameter(self, parameter=None):
        parameter = _CalibrationWidget.parameter(self, parameter)
        parameter.value = self._txt_value.text()
        return parameter

    def setParameter(self, calibration):
        _CalibrationWidget.setParameter(self, calibration)
        self._txt_value.setText(calibration.value)

    def setReadOnly(self, state):
        _CalibrationWidget.setReadOnly(self, state)
        self._txt_value.setReadOnly(state)

    def isReadOnly(self):
        return _CalibrationWidget.isReadOnly(self) and \
            self._txt_value.isReadOnly()

    def hasAcceptableInput(self):
        return _CalibrationWidget.hasAcceptableInput(self) and \
            self._txt_value.hasAcceptableInput()

class CalibrationLinearWidget(_CalibrationWidget):

    def __init__(self, parent=None):
        _CalibrationWidget.__init__(self, CalibrationLinear, parent)
        self.setAccessibleName('linear')

    def _init_ui(self):
        # Widgets
        self._txt_gain = NumericalAttributeLineEdit(self.CLASS.gain)
        self._txt_offset = NumericalAttributeLineEdit(self.CLASS.offset)

        # Layouts
        layout = _CalibrationWidget._init_ui(self)
        layout.addRow('<i>Gain</i>', self._txt_gain)
        layout.addRow('<i>Offset</i>', self._txt_offset)

        # Signals
        self._txt_gain.textEdited.connect(self.edited)
        self._txt_offset.textEdited.connect(self.edited)

        return layout

    def _create_parameter(self):
        return self.CLASS('Quantity', 'm', 0.0, 0.0)

    def parameter(self, parameter=None):
        parameter = _CalibrationWidget.parameter(self, parameter)
        parameter.gain = self._txt_gain.text()
        parameter.offset = self._txt_offset.text()
        return parameter

    def setParameter(self, calibration):
        _CalibrationWidget.setParameter(self, calibration)
        self._txt_gain.setText(calibration.gain)
        self._txt_offset.setText(calibration.offset)

    def setReadOnly(self, state):
        _CalibrationWidget.setReadOnly(self, state)
        self._txt_gain.setReadOnly(state)
        self._txt_offset.setReadOnly(state)

    def isReadOnly(self):
        return _CalibrationWidget.isReadOnly(self) and \
            self._txt_gain.isReadOnly() and \
            self._txt_offset.isReadOnly()

    def hasAcceptableInput(self):
        return _CalibrationWidget.hasAcceptableInput(self) and \
            self._txt_gain.hasAcceptableInput() and \
            self._txt_offset.hasAcceptableInput()

class _CoefficientsLineEdit(_AttributeLineEdit):

    _PATTERN = re.compile(r'^(?P<coef>[\d\.]*)\s*(?P<x>[x]?)(?:[\^](?P<exp>\d*))?$')

    @staticmethod
    def parse_coefficients(text):
        # Parse terms
        terms = {}
        for term in text.split('+'):
            term = term.strip()
            match = _CoefficientsLineEdit._PATTERN.match(term)
            if not match:
                raise ValueError('Unparseable term: %s' % term)

            matchdict = match.groupdict()
            coefficient = float(matchdict['coef'] or (1.0 if matchdict['x'] else 0.0))
            exponent = int(matchdict['exp'] or 1 if matchdict['x'] else 0)

            terms.setdefault(exponent, 0.0)
            terms[exponent] += coefficient

        # Add missing terms
        for exponent in range(max(terms.keys()) + 1):
            if exponent not in terms:
                terms[exponent] = 0.0

        coefficients = []
        for exponent in sorted(terms.keys(), reverse=True):
            coefficients.append(terms[exponent])

        return coefficients

    @staticmethod
    def write_coefficients(coefficients):
        terms = []

        for order, coefficient in enumerate(reversed(coefficients)):
            if coefficient == 0.0: continue
            coefficient_text = str(coefficient) if coefficient != 1.0 else ''
            if order == 0:
                terms.append(coefficient_text)
            elif order == 1:
                terms.append(coefficient_text + "x")
            else:
                terms.append(coefficient_text + "x^" + str(order))

        return ' + '.join(reversed(terms))

    class _Validator(QValidator):

        def validate(self, text, pos):
            try:
                _CoefficientsLineEdit.parse_coefficients(text)
            except:
                return QValidator.Intermediate
            else:
                return QValidator.Acceptable

        def fixup(self, text):
            return text

    def __init__(self, attribute, *args, **kwargs):
        _AttributeLineEdit.__init__(self, attribute, *args, **kwargs)

        self.setValidator(self._Validator())

        self.editingFinished.connect(self._on_editing_finished)

    def _on_editing_finished(self):
        if not self.hasAcceptableInput():
            return
        self.setText(self.text())

    def setText(self, text):
        if text is None:
            text = ''
        else:
            text = _CoefficientsLineEdit.write_coefficients(text)
        return _AttributeLineEdit.setText(self, text)

    def text(self):
        if not self.hasAcceptableInput():
            raise ValueError('Invalid text')

        text = _AttributeLineEdit.text(self)
        if len(text.strip()) == 0:
            return None

        return _CoefficientsLineEdit.parse_coefficients(text)

class CalibrationPolynomialWidget(_CalibrationWidget):

    def __init__(self, parent=None):
        _CalibrationWidget.__init__(self, CalibrationPolynomial, parent)
        self.setAccessibleName('polynomial')

    def _init_ui(self):
        # Widgets
        self._txt_coefficients = _CoefficientsLineEdit(self.CLASS.coefficients)

        # Layout
        layout = _CalibrationWidget._init_ui(self)
        layout.addRow('<i>Coefficients</i>', self._txt_coefficients)

        # Signals
        self._txt_coefficients.textEdited.connect(self.edited)

        return layout

    def _create_parameter(self):
        return self.CLASS('Quantity', 'm', (0,))

    def parameter(self, parameter=None):
        parameter = _CalibrationWidget.parameter(self, parameter)
        parameter.coefficients = self._txt_coefficients.text()
        return parameter

    def setParameter(self, calibration):
        _CalibrationWidget.setParameter(self, calibration)
        self._txt_coefficients.setText(calibration.coefficients)

    def setReadOnly(self, state):
        _CalibrationWidget.setReadOnly(self, state)
        self._txt_coefficients.setReadOnly(state)

    def isReadOnly(self):
        return _CalibrationWidget.isReadOnly(self) and \
            self._txt_coefficients.isReadOnly()

    def hasAcceptableInput(self):
        return _CalibrationWidget.hasAcceptableInput(self) and \
            self._txt_coefficients.hasAcceptableInput()

class _ExplicitLineEdit(_AttributeLineEdit):

    _PATTERN = re.compile(r'[,;]')

    class _Validator(QValidator):

        def validate(self, text, pos):
            try:
                map(float, _ExplicitLineEdit._PATTERN.split(text))
            except:
                return QValidator.Intermediate
            else:
                return QValidator.Acceptable

        def fixup(self, text):
            return text

    def __init__(self, attribute, *args, **kwargs):
        _AttributeLineEdit.__init__(self, attribute, *args, **kwargs)

        self.setValidator(self._Validator())

        self.editingFinished.connect(self._on_editing_finished)

    def _on_editing_finished(self):
        if not self.hasAcceptableInput():
            return
        self.setText(self.text())

    def setText(self, text):
        if text is None:
            text = ''
        else:
            text = ','.join(map(str, text))
        return _AttributeLineEdit.setText(self, text)

    def text(self):
        if not self.hasAcceptableInput():
            raise ValueError('Invalid text')

        text = _AttributeLineEdit.text(self)
        if len(text.strip()) == 0:
            return None

        return self._PATTERN.split(text)

class _ValuesExplicitWidget(_ExplicitLineEdit):

    def text(self):
        return list(map(float, _ExplicitLineEdit.text(self)))

class _LabelsExplicitWidget(_ExplicitLineEdit):
    pass

class CalibrationExplicitWidget(_CalibrationWidget):

    def __init__(self, parent=None):
        _CalibrationWidget.__init__(self, CalibrationExplicit, parent=parent)
        self.setAccessibleName('explicit')

    def _init_ui(self):
        # Widgets
        self._txt_values = _ValuesExplicitWidget(self.CLASS.values)
        self._txt_labels = _LabelsExplicitWidget(self.CLASS.labels)

        # Layouts
        layout = _CalibrationWidget._init_ui(self)
        layout.addRow('Values', self._txt_values)
        layout.addRow('Labels', self._txt_labels)

        # Signals
        self._txt_values.textEdited.connect(self.edited)
        self._txt_labels.textEdited.connect(self.edited)

        return layout

    def _create_parameter(self):
        return self.CLASS('Quantity', 'm', (0,))

    def parameter(self, parameter=None):
        parameter = _CalibrationWidget.parameter(self, parameter)
        parameter.values = self._txt_values.text()
        parameter.labels = self._txt_labels.text()
        return parameter

    def setParameter(self, calibration):
        _CalibrationWidget.setParameter(self, calibration)
        self._txt_values.setText(calibration.values)
        self._txt_labels.setText(calibration.labels)

    def setReadOnly(self, state):
        _CalibrationWidget.setReadOnly(self, state)
        self._txt_values.setReadOnly(state)
        self._txt_labels.setReadOnly(state)

    def isReadOnly(self):
        return _CalibrationWidget.isReadOnly(self) and \
            self._txt_values.isReadOnly() and \
            self._txt_labels.isReadOnly()

    def hasAcceptableInput(self):
        try:
            values = self._txt_values.text()
        except:
            return False

        try:
            labels = self._txt_labels.text()
        except:
            labels = None

        if labels is not None and len(values) != len(labels):
            return False

        return _CalibrationWidget.hasAcceptableInput(self) and \
            self._txt_values.hasAcceptableInput() and \
            self._txt_labels.hasAcceptableInput()

class CalibrationWidget(ParameterWidget):

    def __init__(self, parent=None):
        ParameterWidget.__init__(self, _Calibration, parent)

    def _init_ui(self):
        # Widgets
        self._combobox = QComboBox()
        self._stack = QStackedWidget()

        # Layouts
        layout = ParameterWidget._init_ui(self)
        layout.addRow(self._combobox)
        layout.addRow(self._stack)

        # Register classes
        self._widget_indexes = {}

        for entry_point in iter_entry_points('pyhmsa.gui.spec.condition.calibration'):
            widget_class = entry_point.load(require=False)
            widget = widget_class()
            self._combobox.addItem(widget.accessibleName().title())
            self._widget_indexes[widget.CLASS] = self._stack.addWidget(widget)
            widget.edited.connect(self.edited)

        # Signals
        self._combobox.currentIndexChanged.connect(self._on_combo_box)
        self._combobox.currentIndexChanged.connect(self.edited)

        return layout

    def _on_combo_box(self):
        # Old values
        oldwidget = self._stack.currentWidget()
        try:
            quantity = oldwidget._txt_quantity.text()
        except:
            quantity = None
        try:
            unit = oldwidget._txt_unit.text()
        except:
            unit = None

        # Change widget
        current_index = self._combobox.currentIndex()
        self._stack.setCurrentIndex(current_index)

        # Update values
        widget = self._stack.currentWidget()
        widget._txt_quantity.setText(quantity)
        widget._txt_unit.setText(unit)

    def parameter(self):
        return self._stack.currentWidget().calibration()

    def setParameter(self, calibration):
        index = self._widget_indexes[type(calibration)]
        self._combobox.setCurrentIndex(index)
        self._stack.setCurrentIndex(index)
        self._stack.currentWidget().setParameter(calibration)

    def calibration(self):
        return self.parameter()

    def setCalibration(self, calibration):
        self.setParameter(calibration)

    def setReadOnly(self, state):
        ParameterWidget.setReadOnly(self, state)
        self._combobox.setEnabled(not state)
        self._stack.currentWidget().setReadOnly(state)

    def isReadOnly(self):
        return ParameterWidget.isReadOnly(self) and \
            not self._combobox.isEnabled() and \
            self._stack.currentWidget().isReadOnly()

    def hasAcceptableInput(self):
        return ParameterWidget.hasAcceptableInput(self) and \
            self._stack.currentWidget().hasAcceptableInput()

