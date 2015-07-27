"""
Composition conditions widgets
"""

# Standard library modules.
from collections import OrderedDict
from operator import methodcaller

# Third party modules.
from PySide.QtGui import \
    (QItemDelegate, QTableView, QToolBar, QMessageBox, QComboBox,
     QLineEdit, QDoubleValidator)
from PySide.QtCore import Qt, QAbstractTableModel, QModelIndex

# Local modules.
from pyhmsa.gui.util.periodictable import PeriodicTableDialog
from pyhmsa.gui.util.icon import getIcon
from pyhmsa.gui.spec.condition.condition import _ConditionWidget

from pyhmsa.spec.condition.composition import CompositionElemental

from pyhmsa.util.element_properties import get_symbol

# Globals and constants variables.
from pyhmsa.spec.condition.composition import _COMPOSITION_UNITS

class _CompositionWidget(_ConditionWidget):

    def _init_ui(self):
        # Widgets
        self._cb_unit = QComboBox()
        self._cb_unit.addItems(list(_COMPOSITION_UNITS))

        # Layouts
        layout = _ConditionWidget._init_ui(self)
        layout.addRow('<i>Unit</i>', self._cb_unit)

        # Signals
        self._cb_unit.currentIndexChanged.connect(self.edited)

        return layout

    def parameter(self, parameter=None):
        parameter = _ConditionWidget.parameter(self, parameter)
        parameter.unit = self._cb_unit.currentText()
        return parameter

    def setParameter(self, condition):
        _ConditionWidget.setParameter(self, condition)
        self._cb_unit.setCurrentIndex(self._cb_unit.findText(condition.unit))

    def setReadOnly(self, state):
        _ConditionWidget.setReadOnly(self, state)
        self._cb_unit.setEnabled(not state)

    def isReadOnly(self):
        return _ConditionWidget.isReadOnly(self) and \
            not self._cb_unit.isEnabled()

class CompositionElementalWidget(_CompositionWidget):

    class _CompositionModel(QAbstractTableModel):

        def __init__(self):
            QAbstractTableModel.__init__(self)
            self.composition = OrderedDict()

        def rowCount(self, *args, **kwargs):
            return len(self.composition)

        def columnCount(self, *args, **kwargs):
            return 2

        def data(self, index, role):
            if not index.isValid() or \
                    not (0 <= index.row() < len(self.composition)):
                return None

            if role == Qt.TextAlignmentRole:
                return Qt.AlignCenter

            if role != Qt.DisplayRole:
                return None

            z, fraction = list(self.composition.items())[index.row()]
            column = index.column()
            if column == 0:
                if z is None:
                    return 'none'
                else:
                    return str(get_symbol(z))
            elif column == 1:
                return str(fraction)

        def headerData(self, section , orientation, role):
            if role != Qt.DisplayRole:
                return None
            if orientation == Qt.Horizontal:
                if section == 0:
                    return 'Element'
                elif section == 1:
                    return 'Fraction'
            elif orientation == Qt.Vertical:
                return str(section + 1)

        def flags(self, index):
            if not index.isValid():
                return Qt.ItemIsEnabled

            return Qt.ItemFlags(QAbstractTableModel.flags(self, index) |
                                Qt.ItemIsEditable)

        def setData(self, index, value, role=Qt.EditRole):
            if not index.isValid() or \
                    not (0 <= index.row() < len(self.composition)):
                return False

            z = list(self.composition.keys())[index.row()]
            column = index.column()
            if column == 0:
                if value in self.composition:
                    return False
                fraction = self.composition.pop(z)
                self.composition[value] = fraction
            elif column == 1:
                self.composition[z] = float(value)

            self.dataChanged.emit(index, index)
            return True

        def insertRows(self, row, count=1, parent=None):
            if count == 0:
                return False
            if parent is None:
                parent = QModelIndex()
            self.beginInsertRows(parent, row, row + count - 1)

            if None in self.composition:
                return False
            self.composition[None] = 0.0

            self.endInsertRows()
            return True

        def removeRows(self, row, count=1, parent=None):
            if count == 0:
                return False
            if parent is None:
                parent = QModelIndex()
            self.beginRemoveRows(parent, row, count + row - 1)

            keys = list(self.composition.keys())
            for key in keys[:row] + keys[row + count:]:
                self.composition.pop(key)

            self.endRemoveRows()
            return True

    class _CompositionDelegate(QItemDelegate):

        def __init__(self, parent=None):
            QItemDelegate.__init__(self, parent)

        def createEditor(self, parent, option, index):
            column = index.column()
            if column == 0:
                editor = PeriodicTableDialog(parent)
                editor.setMultipleSelection(False)
                editor.setRequiresSelection(True)
                return editor
            elif column == 1:
                editor = QLineEdit(parent)
                editor.setValidator(QDoubleValidator())
                return editor
            else:
                return QItemDelegate.createEditor(self, parent, option, index)

        def setEditorData(self, editor, index):
            text = index.model().data(index, Qt.DisplayRole)
            column = index.column()
            if column == 0:
                if text != 'none':
                    editor.setSelection(text)
            elif column == 1:
                editor.setText(text)
            else:
                QItemDelegate.setEditorData(self, editor, index)

        def setModelData(self, editor, model, index):
            column = index.column()
            if column == 0:
                model.setData(index, editor.selection())
            elif column == 1:
                model.setData(index, editor.text())
            else:
                return QItemDelegate.setModelData(self, editor, model, index)

    def __init__(self, parent=None):
        _CompositionWidget.__init__(self, CompositionElemental, parent)

    def _init_ui(self):
        # Widgets
        model = self._CompositionModel()

        self._table = QTableView()
        self._table.setModel(model)
        self._table.setItemDelegate(self._CompositionDelegate(self))
        self._table.horizontalHeader().setStretchLastSection(True)

        self._toolbar = QToolBar()
        action_add = self._toolbar.addAction(getIcon("list-add"), "Add layer")
        action_remove = self._toolbar.addAction(getIcon("list-remove"), "Remove layer")

        # Layouts
        layout = _CompositionWidget._init_ui(self)
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

    def _create_parameter(self):
        return self.CLASS('wt%')

    def parameter(self, parameter=None):
        parameter = _CompositionWidget.parameter(self, parameter)
        parameter.update(self._table.model().composition)
        return parameter

    def setParameter(self, condition):
        _CompositionWidget.setParameter(self, condition)
        self._table.model().composition.update(condition)
        self._table.model().reset()

    def setReadOnly(self, state):
        _CompositionWidget.setReadOnly(self, state)
        if state:
            trigger = QTableView.EditTrigger.NoEditTriggers
        else:
            trigger = QTableView.EditTrigger.AllEditTriggers
        self._table.setEditTriggers(trigger)
        self._toolbar.setEnabled(not state)

    def isReadOnly(self):
        return _CompositionWidget.isReadOnly(self) and \
            self._table.editTriggers() == QTableView.EditTrigger.NoEditTriggers and \
            not self._toolbar.isEnabled()
