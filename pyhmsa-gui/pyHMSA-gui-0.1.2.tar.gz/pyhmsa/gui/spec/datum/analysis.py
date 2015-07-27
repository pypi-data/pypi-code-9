"""
Analysis widgets
"""

# Standard library modules.

# Third party modules.
from PySide.QtCore import Qt, QAbstractTableModel

from matplotlib.figure import Figure

# Local modules.
from pyhmsa.gui.spec.datum.datum import _DatumTableWidget, _DatumFigureWidget
from pyhmsa.gui.util.mpl.toolbar import NavigationToolbarQT, NavigationToolbarSnapMixinQT
from pyhmsa.gui.util.mpl.modest_image import imshow as modest_imshow

from pyhmsa.spec.datum.analysis import Analysis0D, Analysis1D, Analysis2D
from pyhmsa.spec.condition.detector import DetectorSpectrometer

# Globals and constants variables.

class _Analysis1DNagivationToolbarQT(NavigationToolbarSnapMixinQT,
                                     NavigationToolbarQT):

    def __init__(self, canvas, parent, coordinates=True):
        NavigationToolbarQT.__init__(self, canvas, parent, coordinates)
        NavigationToolbarSnapMixinQT.__init__(self)

    def _init_toolbar(self):
        NavigationToolbarQT._init_toolbar(self)
        NavigationToolbarSnapMixinQT._init_toolbar(self)

class Analysis0DTableWidget(_DatumTableWidget):

    class _TableModel(QAbstractTableModel):

        def __init__(self, datum):
            QAbstractTableModel.__init__(self)
            self._datum = datum

        def rowCount(self, parent=None):
            return 1

        def columnCount(self, parent=None):
            return 1

        def data(self, index, role):
            if not index.isValid() or not (0 <= index.row() < 1):
                return None
            if role != Qt.DisplayRole:
                return None

            return str(self._datum)

        def headerData(self, section , orientation, role):
            if role != Qt.DisplayRole:
                return None
            if orientation == Qt.Horizontal:
                return 'Value'
            elif orientation == Qt.Vertical:
                return str(section + 1)

    def __init__(self, controller, datum=None, parent=None):
        _DatumTableWidget.__init__(self, Analysis0D, controller, datum, parent)

    def _create_model(self, datum):
        return self._TableModel(datum)

class Analysis1DTableWidget(_DatumTableWidget):

    class _TableModel(QAbstractTableModel):

        def __init__(self, datum):
            QAbstractTableModel.__init__(self)
            self._datum = datum

            conditions = datum.conditions.findvalues(DetectorSpectrometer)
            if conditions:
                self._calibration = next(iter(conditions)).calibration
            else:
                self._calibration = None

        def rowCount(self, parent=None):
            return self._datum.channels

        def columnCount(self, parent=None):
            return 2 if self._calibration is not None else 1

        def data(self, index, role):
            if not index.isValid() or not (0 <= index.row() < self._datum.channels):
                return None
            if role != Qt.DisplayRole:
                return None

            row = index.row()
            column = index.column()
            if self._calibration is not None:
                if column == 0:
                    return str(self._calibration(row))
                elif column == 1:
                    return str(self._datum[row])
            else:
                return str(self._datum[row])

        def headerData(self, section , orientation, role):
            if role != Qt.DisplayRole:
                return None
            if orientation == Qt.Horizontal:
                if self._calibration is not None:
                    if section == 0:
                        return '%s (%s)' % (self._calibration.quantity,
                                            self._calibration.unit)
                    elif section == 1:
                        return 'Value'
                else:
                    return 'Value'
            elif orientation == Qt.Vertical:
                return str(section + 1)

    def __init__(self, controller, datum=None, parent=None):
        _DatumTableWidget.__init__(self, Analysis1D, controller, datum, parent)

    def _create_model(self, datum):
        return self._TableModel(datum)

class Analysis1DGraphWidget(_DatumFigureWidget):

    def __init__(self, controller, datum=None, parent=None):
        _DatumFigureWidget.__init__(self, Analysis1D, controller, datum, parent)

    def _create_figure(self):
        fig = Figure((5.0, 4.0), dpi=100)
        self._ax = None
        self._artist = None
        return fig

    def _create_toolbar(self, canvas):
        return _Analysis1DNagivationToolbarQT(canvas, self.parent())

    def _draw_figure(self, fig, datum):
        if datum is None:
            self._ax = None
            self._artist = None
            return

        # Extract data and labels
        xy = datum.get_xy()
        xlabel = datum.get_xlabel()
        ylabel = datum.get_xlabel()

        # Draw
        if self._artist is None:
            self._ax = fig.add_subplot("111")
            self._artist, = self._ax.plot(xy[:, 0], xy[:, 1], zorder=1)
        else:
            self._artist.set_data((xy[:, 0], xy[:, 1]))
            self._ax.relim()
            self._ax.autoscale(tight=True)

        self._ax.set_xlabel(xlabel)
        self._ax.set_ylabel(ylabel)

class Analysis2DTableWidget(_DatumTableWidget):

    class _TableModel(QAbstractTableModel):

        def __init__(self, datum):
            QAbstractTableModel.__init__(self)
            self._datum = datum

        def rowCount(self, parent=None):
            return self._datum.v

        def columnCount(self, parent=None):
            return self._datum.u

        def data(self, index, role):
            if not index.isValid() or \
                    not (0 <= index.row() < self._datum.v) or \
                    not (0 <= index.column() < self._datum.u):
                return None
            if role != Qt.DisplayRole:
                return None

            row = index.row()
            column = index.column()
            return str(self._datum[column, row])

        def headerData(self, section , orientation, role):
            if role != Qt.DisplayRole:
                return None
            if orientation == Qt.Horizontal:
                return str(section + 1)
            elif orientation == Qt.Vertical:
                return str(section + 1)

    def __init__(self, controller, datum=None, parent=None):
        _DatumTableWidget.__init__(self, Analysis2D, controller, datum, parent)

    def _create_model(self, datum):
        return self._TableModel(datum)

class Analysis2DGraphWidget(_DatumFigureWidget):

    def __init__(self, controller, datum=None, parent=None):
        _DatumFigureWidget.__init__(self, Analysis2D, controller, datum, parent)

    def _create_figure(self):
        fig = Figure((5.0, 4.0), dpi=100)
        self._ax = None
        self._artist = None
        return fig

    def _draw_figure(self, fig, datum):
        if self._artist is None: # First draw
            self._ax = fig.add_axes([0.0, 0.0, 1.0, 1.0])
            self._ax.xaxis.set_visible(False)
            self._ax.yaxis.set_visible(False)
            self._artist = modest_imshow(self._ax, datum.T)
            fig.colorbar(self._artist, shrink=0.8)
        else:
            self._artist.set_data(datum.T)
            self._artist.autoscale()
