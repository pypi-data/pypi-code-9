"""
Specimen position condition widget
"""

# Standard library modules.
from operator import methodcaller

# Third party modules.
from PySide.QtGui import \
    (QHBoxLayout, QVBoxLayout, QLabel, QItemDelegate, QTableView,
     QToolBar, QMessageBox)
from PySide.QtCore import Qt, QAbstractTableModel, QModelIndex

# Local modules.
from pyhmsa.gui.util.parameter import \
    ParameterWidget, NumericalAttributeLineEdit
from pyhmsa.gui.util.icon import getIcon
from pyhmsa.gui.spec.condition.condition import _ConditionWidget

from pyhmsa.spec.condition.specimenposition import SpecimenPosition

# Globals and constants variables.

class SpecimenPositionWidget(_ConditionWidget):

    def __init__(self, inline=False, parent=None):
        self._inline = inline
        _ConditionWidget.__init__(self, SpecimenPosition, parent)

    def _init_ui(self):
        # Widgets
        self._txt_x = NumericalAttributeLineEdit(self._class.x)
        self._txt_y = NumericalAttributeLineEdit(self._class.y)
        self._txt_z = NumericalAttributeLineEdit(self._class.z)
        self._txt_r = NumericalAttributeLineEdit(self._class.r)
        self._txt_t = NumericalAttributeLineEdit(self._class.t)

        # Layouts
        if self._inline:
            layout = QVBoxLayout()

            layout_xyz = QHBoxLayout()
            layout_xyz.addWidget(QLabel('X'))
            layout_xyz.addWidget(self._txt_x)
            layout_xyz.addWidget(QLabel('Y'))
            layout_xyz.addWidget(self._txt_y)
            layout_xyz.addWidget(QLabel('Z'))
            layout_xyz.addWidget(self._txt_z)

            layout_rt = QHBoxLayout()
            layout_rt.addWidget(QLabel('R'))
            layout_rt.addWidget(self._txt_r)
            layout_rt.addWidget(QLabel('T'))
            layout_rt.addWidget(self._txt_t)

            layout.addLayout(layout_xyz)
            layout.addLayout(layout_rt)
        else:
            layout = _ConditionWidget._init_ui(self)
            layout.addRow('X', self._txt_x)
            layout.addRow('Y', self._txt_y)
            layout.addRow('Z', self._txt_z)
            layout.addRow('R', self._txt_r)
            layout.addRow('T', self._txt_t)

        # Signals
        self._txt_x.textEdited.connect(self.edited)
        self._txt_y.textEdited.connect(self.edited)
        self._txt_z.textEdited.connect(self.edited)
        self._txt_r.textEdited.connect(self.edited)
        self._txt_t.textEdited.connect(self.edited)

        return layout

    def parameter(self, parameter=None):
        parameter = _ConditionWidget.parameter(self, parameter)
        parameter.x = self._txt_x.text()
        parameter.y = self._txt_y.text()
        parameter.z = self._txt_z.text()
        parameter.r = self._txt_r.text()
        parameter.t = self._txt_t.text()
        return parameter

    def setParameter(self, condition):
        _ConditionWidget.setParameter(self, condition)
        self._txt_x.setText(condition.x)
        self._txt_y.setText(condition.y)
        self._txt_z.setText(condition.z)
        self._txt_r.setText(condition.r)
        self._txt_t.setText(condition.t)

class SpecimenPositionListWidget(ParameterWidget):

    class _SpecimenPositionModel(QAbstractTableModel):

        def __init__(self):
            QAbstractTableModel.__init__(self)
            self.positions = []

        def rowCount(self, *args, **kwargs):
            return len(self.positions)

        def columnCount(self, *args, **kwargs):
            return 5

        def data(self, index, role):
            if not index.isValid() or not (0 <= index.row() < len(self.positions)):
                return None
            if role != Qt.DisplayRole:
                return None

            position = self.positions[index.row()]
            column = index.column()
            if column == 0:
                return str(position.x) if position.x is not None else ''
            elif column == 1:
                return str(position.y) if position.y is not None else ''
            elif column == 2:
                return str(position.z) if position.z is not None else ''
            elif column == 3:
                return str(position.r) if position.r is not None else ''
            elif column == 4:
                return str(position.t) if position.t is not None else ''

        def headerData(self, section , orientation, role):
            if role != Qt.DisplayRole:
                return None
            if orientation == Qt.Horizontal:
                if section == 0:
                    return 'X'
                elif section == 1:
                    return 'Y'
                elif section == 2:
                    return 'Z'
                elif section == 3:
                    return 'R'
                elif section == 4:
                    return 'T'
            elif orientation == Qt.Vertical:
                return str(section + 1)

        def flags(self, index):
            if not index.isValid():
                return Qt.ItemIsEnabled

            return Qt.ItemFlags(QAbstractTableModel.flags(self, index) |
                                Qt.ItemIsEditable)

        def setData(self, index, value, role=Qt.EditRole):
            if not index.isValid() or \
                    not (0 <= index.row() < len(self.positions)):
                return False

            position = self.positions[index.row()]
            column = index.column()
            if column == 0:
                position.x = value
            elif column == 1:
                position.y = value
            elif column == 2:
                position.z = value
            elif column == 3:
                position.r = value
            elif column == 4:
                position.t = value

            return True

        def insertRows(self, row, count=1, parent=None):
            if count == 0:
                return False
            if parent is None:
                parent = QModelIndex()
            self.beginInsertRows(parent, row, row + count - 1)

            for i in range(count):
                self.positions.insert(row + i, SpecimenPosition())

            self.endInsertRows()
            return True

        def removeRows(self, row, count=1, parent=None):
            if count == 0:
                return False
            if parent is None:
                parent = QModelIndex()
            self.beginRemoveRows(parent, row, row + count - 1)

            self.positions = self.positions[:row] + self.positions[row + count:]

            self.endRemoveRows()
            return True

    class _SpecimenPositionDelegate(QItemDelegate):

        def __init__(self, parent=None):
            QItemDelegate.__init__(self, parent)

        def createEditor(self, parent, option, index):
            column = index.column()
            if column == 0:
                return NumericalAttributeLineEdit(SpecimenPosition.x, parent)
            elif column == 1:
                return NumericalAttributeLineEdit(SpecimenPosition.y, parent)
            elif column == 2:
                return NumericalAttributeLineEdit(SpecimenPosition.y, parent)
            elif column == 3:
                return NumericalAttributeLineEdit(SpecimenPosition.y, parent)
            elif column == 4:
                return NumericalAttributeLineEdit(SpecimenPosition.y, parent)
            else:
                return QItemDelegate.createEditor(self, parent, option, index)

        def setEditorData(self, editor, index):
            text = index.model().data(index, Qt.DisplayRole)
            column = index.column()
            if column == 0:
                editor.setText(text)
            elif column == 1:
                editor.setText(text)
            elif column == 2:
                editor.setText(text)
            elif column == 3:
                editor.setText(text)
            elif column == 4:
                editor.setText(text)
            else:
                QItemDelegate.setEditorData(self, editor, index)

        def setModelData(self, editor, model, index):
            column = index.column()
            if column == 0:
                model.setData(index, editor.text())
            elif column == 1:
                model.setData(index, editor.text())
            elif column == 2:
                model.setData(index, editor.text())
            elif column == 3:
                model.setData(index, editor.text())
            elif column == 4:
                model.setData(index, editor.text())
            else:
                return QItemDelegate.setModelData(self, editor, model, index)

    def __init__(self, parent=None):
        ParameterWidget.__init__(self, object, parent)

    def _init_ui(self):
        # Widgets
        self._table = QTableView()
        self._table.setModel(self._SpecimenPositionModel())
        self._table.setItemDelegate(self._SpecimenPositionDelegate(self))
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

        return layout

    def _on_add(self):
        index = self._table.selectionModel().currentIndex()
        model = self._table.model()
        model.insertRows(index.row() + 1)

    def _on_remove(self):
        selection = self._table.selectionModel().selection().indexes()
        if len(selection) == 0:
            QMessageBox.warning(self, "Specimen position", "Select a position")
            return

        model = self._table.model()
        for row in sorted(map(methodcaller('row'), selection), reverse=True):
            model.removeRow(row)

    def parameter(self):
        positions = []
        for position in self._table.model().positions:
            positions.append(SpecimenPosition(position.x, position.y, position.z,
                                              position.r, position.t))
        return positions

    def setParameter(self, positions):
        model = self._table.model()
        model.positions = positions
        model.reset()

    def positions(self):
        return self.parameter()

    def setPositions(self, positions):
        self.setParameter(positions)

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
