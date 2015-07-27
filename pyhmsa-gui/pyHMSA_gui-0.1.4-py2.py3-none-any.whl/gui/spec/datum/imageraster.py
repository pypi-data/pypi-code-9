"""
Image raster widgets
"""

# Standard library modules.

# Third party modules.
from PySide.QtGui import \
    QSlider, QFormLayout, QHBoxLayout, QRadioButton, QSplitter, QSizePolicy
from PySide.QtCore import Qt, QAbstractTableModel, Signal

import matplotlib
from matplotlib.figure import Figure

import numpy as np

# Local modules.
from pyhmsa.gui.spec.datum.datum import \
    _DatumWidget, _DatumTableWidget, _DatumFigureWidget
from pyhmsa.gui.spec.datum.analysis import \
    Analysis1DTableWidget, Analysis1DGraphWidget
from pyhmsa.gui.util.mpl.modest_image import imshow as modest_imshow
from pyhmsa.gui.util.mpl.toolbar import \
    (NavigationToolbarQT, NavigationToolbarColorbarMixinQT,
     NavigationToolbarScalebarMixinQT)
from pyhmsa.gui.util.mpl.scalebar import ScaleBar

from pyhmsa.spec.datum.analysis import Analysis1D
from pyhmsa.spec.datum.imageraster import ImageRaster2D, ImageRaster2DSpectral
from pyhmsa.spec.condition.acquisition import AcquisitionRasterXY
from pyhmsa.type.numerical import convert_unit

# Globals and constants variables.

class _ImageRaster2DNavigationToolbarQT(NavigationToolbarColorbarMixinQT,
                                        NavigationToolbarScalebarMixinQT,
                                        NavigationToolbarQT):

    def __init__(self, canvas, parent, coordinates=True):
        NavigationToolbarQT.__init__(self, canvas, parent, coordinates)
        NavigationToolbarColorbarMixinQT.__init__(self)
        NavigationToolbarScalebarMixinQT.__init__(self)

    def _init_toolbar(self):
        NavigationToolbarQT._init_toolbar(self)
        NavigationToolbarColorbarMixinQT._init_toolbar(self)
        NavigationToolbarScalebarMixinQT._init_toolbar(self)

class ImageRaster2DTableWidget(_DatumTableWidget):

    class _TableModel(QAbstractTableModel):

        def __init__(self, datum):
            QAbstractTableModel.__init__(self)
            self._datum = datum

        def rowCount(self, parent=None):
            return self._datum.y

        def columnCount(self, parent=None):
            return self._datum.x

        def data(self, index, role):
            if not index.isValid() or \
                    not (0 <= index.row() < self._datum.y) or \
                    not (0 <= index.column() < self._datum.x):
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
        _DatumTableWidget.__init__(self, ImageRaster2D, controller,
                                   datum, parent)

    def _create_model(self, datum):
        return self._TableModel(datum)

class ImageRaster2DGraphWidget(_DatumFigureWidget):

    def __init__(self, controller, datum=None, parent=None):
        _DatumFigureWidget.__init__(self, ImageRaster2D, controller,
                                    datum, parent)

    def _create_toolbar(self, canvas):
        self._toolbar = _ImageRaster2DNavigationToolbarQT(canvas, self.parent())
        self._toolbar.colorbar_changed.connect(self._on_colorbar_changed)
        self._toolbar.scalebar_changed.connect(self._on_scalebar_changed)
        return self._toolbar

    def _create_figure(self):
        fig = Figure((5.0, 4.0), dpi=100)
        self._ax = None
        self._artist = None
        return fig

    def _create_colorbar(self, fig):
        settings = self.controller.settings

        colorbar = fig.colorbar(self._artist, ax=self._ax, shrink=0.8)
        colorbar.ax.set_visible(settings.valueBool('colorbar/visible', True))

        self._toolbar.set_colorbar(colorbar)

        return colorbar

    def _create_scalebar(self, datum):
        acqs = datum.conditions.findvalues(AcquisitionRasterXY)
        if not acqs:
            return None
        acq = next(iter(acqs))
        dx_m = convert_unit('m', acq.step_size_x)

        settings = self.controller.settings
        visible = settings.valueBool('scalebar/visible', True)
        length_fraction = float(settings.value('scalebar/lengthFraction', 0.2))
        height_fraction = float(settings.value('scalebar/heightFraction', 0.01))
        location = int(settings.value('scalebar/location', 3))
        color = settings.valueColor('scalebar/color', 'w')
        box_color = settings.valueColor('scalebar/boxColor', 'k')
        box_alpha = float(settings.value('scalebar/boxAlpha', 0.5))
        label_top = settings.valueBool('scalebar/labelTop', False)

        scalebar = ScaleBar(dx_m,
                            length_fraction=length_fraction,
                            height_fraction=height_fraction,
                            location=location,
                            color=color,
                            box_color=box_color,
                            box_alpha=box_alpha,
                            label_top=label_top)
        scalebar.set_visible(visible)

        self._toolbar.set_scalebar(scalebar)

        return scalebar

    def _draw_figure(self, fig, datum):
        if datum is None:
            self._ax = None
            self._artist = None
            return

        if self._artist is None: # First draw
            self._ax = fig.add_subplot("111")
            fig.subplots_adjust(0.0, 0.0, 1.0, 1.0)

            self._ax.xaxis.set_visible(False)
            self._ax.yaxis.set_visible(False)

            settings = self.controller.settings
            cmap = settings.value('colorbar/colormap', 'jet') or 'jet'
            self._artist = modest_imshow(self._ax, datum.T, cmap=cmap)

            scalebar = self._create_scalebar(datum)
            if scalebar is not None:
                self._ax.add_artist(scalebar)

            self._create_colorbar(fig)

        else:
            self._artist.set_data(datum.T)
            self._artist.autoscale()

    def _on_colorbar_changed(self, visible, colormap):
        settings = self.controller.settings
        settings.setValue('colorbar/visible', visible)
        settings.setValue('colorbar/colormap', colormap)

    def _on_scalebar_changed(self, visible, location,
                             length_fraction, height_fraction,
                             label_top, color, box_color, box_alpha):
        settings = self.controller.settings
        settings.setValue('scalebar/visible', visible)
        settings.setValue('scalebar/location', location)
        settings.setValue('scalebar/lengthFraction', length_fraction)
        settings.setValue('scalebar/heightFraction', height_fraction)
        settings.setValueColor('scalebar/color', color)
        settings.setValueColor('scalebar/boxColor', box_color)
        settings.setValue('scalebar/boxAlpha', box_alpha)
        settings.setValue('scalebar/labelTop', label_top)

class _ImageRaster2DSpectralWidget(_DatumWidget):

    MODE_SUM = 'sum'
    MODE_MAX = 'max'
    MODE_SINGLE = 'single'
    MODE_RANGE = 'range'

    valueSelected = Signal(int, int)

    def __init__(self, controller, datum=None, parent=None):
        self._datum = None
        _DatumWidget.__init__(self, ImageRaster2DSpectral, controller,
                              datum, parent)

    def _init_ui(self):
        # Widgets
        self._rdb_sum = QRadioButton("Sum")
        self._rdb_sum.setChecked(True)
        self._rdb_max = QRadioButton("Maximum")
        self._rdb_single = QRadioButton("Single")
        self._rdb_range = QRadioButton("Range")

        self._sld_start = QSlider(Qt.Orientation.Horizontal)
        self._sld_start.setTickPosition(QSlider.TicksBelow)
        self._sld_start.setEnabled(False)

        self._sld_end = QSlider(Qt.Orientation.Horizontal)
        self._sld_end.setTickPosition(QSlider.TicksBelow)
        self._sld_end.setEnabled(False)

        self._wdg_imageraster2d = self._create_imageraster2d_widget()
        self._wdg_analysis = self._create_analysis1d_widget()

        # Layouts
        layout = _DatumWidget._init_ui(self)

        sublayout = QHBoxLayout()
        sublayout.addWidget(self._rdb_sum)
        sublayout.addWidget(self._rdb_max)
        sublayout.addWidget(self._rdb_single)
        sublayout.addWidget(self._rdb_range)
        layout.addLayout(sublayout)

        sublayout = QFormLayout()
        sublayout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow) # Fix for Mac OS
        sublayout.addRow('Channels (Start)', self._sld_start)
        sublayout.addRow('Channels (End)', self._sld_end)
        layout.addLayout(sublayout)

        splitter = QSplitter()
        splitter.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        splitter.addWidget(self._wdg_imageraster2d)
        splitter.addWidget(self._wdg_analysis)
        layout.addWidget(splitter)

        # Signals
        self._rdb_sum.toggled.connect(self._on_mode_sum)
        self._rdb_max.toggled.connect(self._on_mode_max)
        self._rdb_single.toggled.connect(self._on_mode_single)
        self._rdb_range.toggled.connect(self._on_mode_range)

        self._sld_start.valueChanged.connect(self._on_slide_start)
        self._sld_end.valueChanged.connect(self._on_slide_end)

        self.valueSelected.connect(self._on_value_selected)

        # Defaults
        self.setMode(self.MODE_SUM)

        return layout

    def _create_analysis1d_widget(self):
        raise NotImplementedError

    def _create_imageraster2d_widget(self):
        raise NotImplementedError

    def _on_mode_sum(self, checked):
        if checked:
            self.setMode(self.MODE_SUM)

    def _on_mode_max(self, checked):
        if checked:
            self.setMode(self.MODE_MAX)

    def _on_mode_single(self, checked):
        if checked:
            self.setMode(self.MODE_SINGLE)

    def _on_mode_range(self, checked):
        if checked:
            self.setMode(self.MODE_RANGE)

    def _update_data(self, mode=None):
        if mode is None:
            mode = self.mode()

        if mode == self.MODE_SUM:
            self._update_mode_sum()
        elif mode == self.MODE_MAX:
            self._update_mode_max()
        elif mode == self.MODE_SINGLE:
            self._update_mode_single()
        elif mode == self.MODE_RANGE:
            self._update_mode_range()

    def _update_mode_sum(self):
        if self._datum is None:
            return
        subdatum = np.sum(self._datum, 2)
        self._wdg_imageraster2d.setDatum(subdatum)

    def _update_mode_max(self):
        if self._datum is None:
            return
        subdatum = np.amax(self._datum, 2)
        self._wdg_imageraster2d.setDatum(subdatum)

    def _update_mode_single(self):
        if self._datum is None:
            return
        channel = self._sld_start.value()
        subdatum = self._datum[:, :, channel]
        self._wdg_imageraster2d.setDatum(subdatum)

    def _update_mode_range(self):
        if self._datum is None:
            return
        start = self._sld_start.value()
        end = self._sld_end.value()
        start2 = min(start, end)
        end2 = max(start, end)
        subdatum = np.sum(self._datum[:, :, start2:end2 + 1], 2)
        self._wdg_imageraster2d.setDatum(subdatum)

    def _on_slide_start(self, channel):
        if self._rdb_single.isChecked():
            self._update_mode_single()
        elif self._rdb_range.isChecked():
            self._update_mode_range()

    def _on_slide_end(self, channel):
        self._update_mode_range()

    def _on_value_selected(self, x, y):
        if self._datum is None:
            return
        subdatum = self._datum[x, y]
        self._wdg_analysis.setDatum(subdatum.view(Analysis1D))
        self._update_data()

    def setDatum(self, datum):
        _DatumWidget.setDatum(self, datum)
        self._datum = datum

        self._sld_start.setMaximum(datum.channels - 1)
        self._sld_end.setMaximum(datum.channels - 1)

        self._update_data()

    def setMode(self, mode):
        rsum = rmax = rsingle = rrange = False
        sstart = send = False
        if mode == self.MODE_SUM:
            rsum = True
        elif mode == self.MODE_MAX:
            rmax = True
        elif mode == self.MODE_SINGLE:
            rsingle = True
            sstart = True
        elif mode == self.MODE_RANGE:
            rrange = True
            sstart = send = True
        else:
            raise ValueError('Unknown mode')

        self._rdb_sum.setChecked(rsum)
        self._rdb_max.setChecked(rmax)
        self._rdb_single.setChecked(rsingle)
        self._rdb_range.setChecked(rrange)
        self._sld_start.setEnabled(sstart)
        self._sld_end.setEnabled(send)

        self._update_data(mode)

    def mode(self):
        if self._rdb_sum.isChecked():
            return self.MODE_SUM
        elif self._rdb_max.isChecked():
            return self.MODE_MAX
        elif self._rdb_single.isChecked():
            return self.MODE_SINGLE
        elif self._rdb_range.isChecked():
            return self.MODE_RANGE
        else:
            raise ValueError('Unknown mode')

class ImageRaster2DSpectralTableWidget(_ImageRaster2DSpectralWidget):

    def _create_imageraster2d_widget(self):
        widget = ImageRaster2DTableWidget(self.controller)
        widget._table.clicked.connect(self._on_table_clicked)
        return widget

    def _create_analysis1d_widget(self):
        return Analysis1DTableWidget(self.controller)

    def _on_table_clicked(self, index):
        self.valueSelected.emit(index.column(), index.row())

class _Analysis1DGraphWidget2(Analysis1DGraphWidget):

    def _create_figure(self):
        fig = Analysis1DGraphWidget._create_figure(self)
        self._ax_single = None
        self._ax_range = None
        return fig

    def _draw_figure(self, fig, datum):
        Analysis1DGraphWidget._draw_figure(self, fig, datum)

        if datum is None:
            self._ax_single = None
            self._ax_range = None
            return

        color = matplotlib.rcParams['axes.color_cycle'][1]

        self._ax_single = self._ax.axvline(0, lw=3, color=color, zorder=3)
        self._ax_single.set_visible(False)

        self._ax_range = self._ax.axvspan(0, 0, alpha=0.5, facecolor=color, zorder=3)
        self._ax_range.set_visible(False)

    def setMode(self, mode):
        if self._ax_single is None or self._ax_range is None:
            return

        vsingle = vrange = False
        if mode == _ImageRaster2DSpectralWidget.MODE_SINGLE:
            vsingle = True
        elif mode == _ImageRaster2DSpectralWidget.MODE_RANGE:
            vrange = True

        self._ax_single.set_visible(vsingle)
        self._ax_range.set_visible(vrange)

        self._canvas.draw()

    def setSinglePosition(self, channel):
        if self._artist is None or self._ax_single is None:
            return

        self._ax_single.set_visible(True)

        xs = self._artist.get_xdata()
        ys = self._artist.get_ydata()

        x = xs[channel]
        ymin = min(ys); ymax = max(ys)
        self._ax_single.set_xdata([x, x])
        self._ax_single.set_ydata([ymin, ymax])

        self._canvas.draw()

    def setRange(self, start, end):
        if self._artist is None or self._ax_range is None:
            return

        self._ax_range.set_visible(True)

        xs = self._artist.get_xdata()
        ys = self._artist.get_ydata()

        xmin = xs[start]; xmax = xs[end]
        ymin = min(ys); ymax = max(ys)
        self._ax_range.set_xy([[xmin, ymin],
                               [xmin, ymax],
                               [xmax, ymax],
                               [xmax, ymin]])

        self._canvas.draw()

class ImageRaster2DSpectralGraphWidget(_ImageRaster2DSpectralWidget):

    def _create_imageraster2d_widget(self):
        widget = ImageRaster2DGraphWidget(self.controller)
        widget._canvas.mpl_connect("button_release_event", self._onFigureClicked)
        return widget

    def _create_analysis1d_widget(self):
        return _Analysis1DGraphWidget2(self.controller)

    def _onFigureClicked(self, event):
        if not event.inaxes:
            return
        self.valueSelected.emit(event.xdata, event.ydata)

    def _update_mode_single(self):
        _ImageRaster2DSpectralWidget._update_mode_single(self)

        channel = self._sld_start.value()
        self._wdg_analysis.setSinglePosition(channel)

    def _update_mode_range(self):
        _ImageRaster2DSpectralWidget._update_mode_range(self)

        start = self._sld_start.value()
        end = self._sld_end.value()
        self._wdg_analysis.setRange(start, end)

    def setMode(self, mode):
        _ImageRaster2DSpectralWidget.setMode(self, mode)
        self._wdg_analysis.setMode(mode)


