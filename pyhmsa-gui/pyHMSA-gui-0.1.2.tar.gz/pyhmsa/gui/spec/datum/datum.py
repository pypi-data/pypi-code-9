"""
Base datum widgets
"""

# Standard library modules.

# Third party modules.
from PySide.QtGui import QWidget, QVBoxLayout, QTableView, QHeaderView, QSizePolicy
from PySide.QtCore import Qt

from matplotlib.backends.backend_qt4agg import \
    (FigureCanvasQTAgg as FigureCanvas,
     NavigationToolbar2QT as NavigationToolbar)

# Local modules.

# Globals and constants variables.

class _DatumWidget(QWidget):

    def __init__(self, clasz, controller, datum=None, parent=None):
        QWidget.__init__(self, parent)

        name = clasz.TEMPLATE
        if clasz.CLASS is not None:
            name += ' (%s)' % clasz.CLASS
        self.setAccessibleName(name)

        # Variables
        self._class = clasz
        self._controller = controller

        # Layouts
        layout = QVBoxLayout()
        layout.addLayout(self._init_ui()) # Initialize widgets
        self.setLayout(layout)

        # Defaults
        self.setDatum(datum)

    def _init_ui(self):
        return QVBoxLayout()

    def setDatum(self, datum):
        """
        Sets the datum. Note that ``datum`` could be ``None``.
        """
        pass

    @property
    def CLASS(self):
        return self._class

    @property
    def controller(self):
        return self._controller

class _DatumTableWidget(_DatumWidget):

    def __init__(self, clasz, controller, datum=None, parent=None):
        _DatumWidget.__init__(self, clasz, controller, datum, parent)

    def _init_ui(self):
        # Widgets
        self._table = QTableView()
        self._table.horizontalHeader().setResizeMode(QHeaderView.Stretch)

        # Layouts
        layout = _DatumWidget._init_ui(self)
        layout.addWidget(self._table)

        return layout

    def _create_model(self, datum):
        raise NotImplementedError

    def setDatum(self, datum):
        _DatumWidget.setDatum(self, datum)

        if datum is not None:
            model = self._create_model(datum)
        else:
            model = None
        self._table.setModel(model)

class _DatumFigureWidget(_DatumWidget):

    def __init__(self, clasz, controller, datum=None, parent=None):
        _DatumWidget.__init__(self, clasz, controller, datum, parent)

    def _init_ui(self):
        # Widgets
        figure = self._create_figure()
        self._canvas = FigureCanvas(figure)
        self._canvas.setFocusPolicy(Qt.StrongFocus)
        self._canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._canvas.updateGeometry()

        self.toolbar = self._create_toolbar(self._canvas)

        # Layouts
        layout = _DatumWidget._init_ui(self)
        layout.addWidget(self._canvas)
        layout.addWidget(self.toolbar)

        return layout

    def _create_figure(self):
        raise NotImplementedError

    def _create_toolbar(self, canvas):
        return NavigationToolbar(canvas, self.parent())

    def _draw_figure(self, fig, datum):
        raise NotImplementedError

    def setDatum(self, datum):
        _DatumWidget.setDatum(self, datum)
        if datum is None:
            self._canvas.figure.clear()
        else:
            self._draw_figure(self._canvas.figure, datum)
        self._canvas.draw()
