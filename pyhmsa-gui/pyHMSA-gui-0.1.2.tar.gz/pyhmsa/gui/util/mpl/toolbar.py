"""
Extension of matplotlib backend
"""

# Standard library modules.
import os
from operator import itemgetter

# Third party modules.
import six

import numpy as np

from PySide.QtCore import Qt, Signal
from PySide.QtGui import \
    (QAction, QDialog, QComboBox, QVBoxLayout, QDialogButtonBox, QCheckBox,
     QFormLayout, QSlider, QLabel, QFileDialog, QSpinBox, QHBoxLayout,
     QMessageBox, QWidget, QButtonGroup, QRadioButton)

import matplotlib
import matplotlib.cm as cm
import matplotlib.colors as colors
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as _NavigationToolbar2QT

# Local modules.
from pyhmsa.gui.util.icon import getIcon
from pyhmsa.gui.util.layout import horizontal
from pyhmsa.gui.util.widget import ColorDialogButton
from pyhmsa.gui.util.mpl.scalebar import ScaleBar
from pyhmsa.gui.util.mpl.color import \
    convert_color_mpl_to_qt, convert_color_qt_to_mpl

# Globals and constants variables.

class _SaveDialog(QFileDialog):

    def __init__(self, parent):
        QFileDialog.__init__(self, parent)
        self.setFileMode(QFileDialog.FileMode.AnyFile)
        self.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)

        # Widgets
        self._chk_tight = QCheckBox('Tight layout')

        self._txt_dpi = QSpinBox()
        self._txt_dpi.setRange(1, 10000)
        self._txt_dpi.setSingleStep(50)
        self._txt_dpi.setSuffix('dpi')
        self._txt_dpi.setValue(100)

        # Layouts
        layout = self.layout()

        lyt_extras = QHBoxLayout()
        lyt_extras.addWidget(QLabel('Extra options'))
        lyt_extras.addWidget(self._chk_tight)
        lyt_extras.addWidget(QLabel('Resolution'))
        lyt_extras.addWidget(self._txt_dpi)
        layout.addLayout(lyt_extras, layout.rowCount(), 0, 1, layout.columnCount())

        self.setLayout(layout)

    def tightLayout(self):
        return self._chk_tight.isChecked()

    def setTightLayout(self, tight):
        self._chk_tight.setChecked(tight)

    def dpi(self):
        return self._txt_dpi.value()

    def setDpi(self, dpi):
        self._txt_dpi.setValue(dpi)

class NavigationToolbarQT(_NavigationToolbar2QT):

    def _get_save_name_filters(self):
        filters = []
        selected_filter = None
        filetypes = self.canvas.get_supported_filetypes_grouped()
        sorted_filetypes = list(six.iteritems(filetypes))
        sorted_filetypes.sort()
        default_filetype = self.canvas.get_default_filetype()

        for name, exts in sorted_filetypes:
            exts_list = " ".join(['*.%s' % ext for ext in exts])
            filter_ = '%s (%s)' % (name, exts_list)
            if default_filetype in exts:
                selected_filter = filter_
            filters.append(filter_)

        return filters, selected_filter

    def save_figure(self, *args):
        dialog = _SaveDialog(self.parent)
        dialog.setWindowTitle("Choose a filename to save to")
        dialog.setDpi(matplotlib.rcParams.get('savefig.dpi',
                                              self.canvas.figure.dpi))
        dialog.setTightLayout(matplotlib.rcParams.get('savefig.bbox', None) == 'tight')

        filters, selected_filter = self._get_save_name_filters()
        dialog.setNameFilters(filters)
        dialog.selectNameFilter(selected_filter)

        startpath = matplotlib.rcParams.get('savefig.directory', '')
        startpath = os.path.expanduser(startpath)
        start = os.path.join(startpath, self.canvas.get_default_filename())
        dialog.selectFile(start)

        if not dialog.exec_():
            return

        fnames = dialog.selectedFiles()
        if len(fnames) != 1:
            return
        fname = fnames[0]

        dpi = dialog.dpi()
        bbox_inches = 'tight' if dialog.tightLayout() else None

        # Store default values
        if startpath == '':
            # explicitly missing key or empty str signals to use cwd
            matplotlib.rcParams['savefig.directory'] = startpath
        else:
            # save dir for next time
            savefig_dir = os.path.dirname(six.text_type(fname))
            matplotlib.rcParams['savefig.directory'] = savefig_dir

        matplotlib.rcParams['savefig.dpi'] = dpi
        matplotlib.rcParams['savefig.bbox'] = bbox_inches

        # Save
        try:
            self.canvas.print_figure(six.text_type(fname),
                                 dpi=dpi, bbox_inches=bbox_inches)
        except Exception as e:
            QMessageBox.critical(
                self, "Error saving file", str(e),
                QMessageBox.Ok, QMessageBox.NoButton)

class NavigationToolbarSnapMixin(object):

    def __init__(self):
        self._snap_cross = {}

    def _clear_snap(self):
        for axes, (crossh, crossv) in self._snap_cross.items():
            axes.lines.remove(crossh)
            axes.lines.remove(crossv)
        self._snap_cross.clear()
        self.draw()

    def pan(self, *args):
        self._clear_snap()
        super().pan(*args)

    def zoom(self, *args):
        print('xoom')
        self._clear_snap()
        super().zoom(*args)

    def snap(self, *args):
        if self._active == 'SNAP':
            self._active = None
        else:
            self._active = 'SNAP'

        if self._idPress is not None:
            self._idPress = self.canvas.mpl_disconnect(self._idPress)

        if self._idRelease is not None:
            self._idRelease = self.canvas.mpl_disconnect(self._idRelease)

        self._clear_snap()

        if self._active:
            self.mode = 'snap'
            self.canvas.widgetlock(self)

            for axes in self.canvas.figure.get_axes():
                xmin, _ = axes.get_xlim()
                ymin, _ = axes.get_ylim()
                color = matplotlib.rcParams.get('snap.color', 'r')
                lw = matplotlib.rcParams.get('snap.linewidth', 2)
                crossh = axes.axhline(ymin, color=color, lw=lw)
                crossv = axes.axvline(xmin, color=color, lw=lw)
                crossh.set_visible(False)
                crossv.set_visible(False)
                self._snap_cross[axes] = (crossh, crossv)
        else:
            self.mode = ''
            self.canvas.widgetlock.release(self)

        for a in self.canvas.figure.get_axes():
            a.set_navigate_mode(self._active)

        self.set_message(self.mode)

    def mouse_move(self, event):
        if self.mode != 'snap':
            super().mouse_move(event)
            return

        for axes, (crossh, crossv) in self._snap_cross.items():
            crossh.set_visible(event.inaxes == axes)
            crossv.set_visible(event.inaxes == axes)

        if event.inaxes is None:
            super().mouse_move(event)
            self.draw()
            return

        x = event.xdata
        y = event.ydata

        xlines = []
        ylines = []
        for line in event.inaxes.lines:
            if line in self._snap_cross[event.inaxes]: continue
            xs = line.get_xdata()
            ys = line.get_ydata()
            index = np.abs(xs - x).argmin()
            xlines.append(xs[index])
            ylines.append(ys[index])

        index = np.abs(np.array(ylines) - y).argmin()
        x = xlines[index]
        y = ylines[index]

        crossh, crossv = self._snap_cross[event.inaxes]
        crossh.set_ydata([y, y])
        crossv.set_xdata([x, x])

        s = event.inaxes.format_coord(x, y)
        self.set_message('%s, %s' % (self.mode, s))

        self.draw()

class NavigationToolbarSnapMixinQT(NavigationToolbarSnapMixin):

    def _init_toolbar(self):
        a = QAction(getIcon('snap'), 'Snap', self)
        a.setCheckable(True)
        a.setToolTip('Snap to data')
        a.triggered.connect(self.snap)
        self._actions['snap'] = a
        self.insertAction(self._actions['pan'], a)

    def snap(self, *args):
        super().snap(*args)
        self._update_buttons_checked()

    def _update_buttons_checked(self):
        super()._update_buttons_checked()
        self._actions['snap'].setChecked(self._active == 'SNAP')

class ColorbarWidget(QWidget):

    POSITION_INSIDE = 'inside'
    POSITION_OUTSIDE = 'outside'

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        # Variables
        cmaps = sorted(key for key in cm.cmap_d.keys() \
                       if not key.endswith('_r'))

        # Widgets
        self._chk_visible = QCheckBox('Visible')

        self._cb_colormap = QComboBox()
        self._cb_colormap.addItems(cmaps)

        self._chk_reverse = QCheckBox('Reverse')

        self._rb_position = QButtonGroup()
        self._rb_position.addButton(QRadioButton('inside'), 0)
        self._rb_position.addButton(QRadioButton('outside'), 1)

        # Layouts
        layout = QFormLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addRow(self._chk_visible)
        layout.addRow('Color map', horizontal(self._cb_colormap, self._chk_reverse))

        sublayout = QVBoxLayout()
        for button in self._rb_position.buttons():
            sublayout.addWidget(button)
        layout.addRow('Position', sublayout)

        self.setLayout(layout)

        # Defaults
        self._rb_position.button(0).setChecked(True)

    def colormap(self):
        colormap = self._cb_colormap.currentText()
        if self._chk_reverse.isChecked():
            colormap += '_r'
        return colormap

    def setColormap(self, colormap):
        if isinstance(colormap, colors.Colormap):
            colormap = colormap.name

        if colormap.endswith('_r'):
            colormap = colormap[:-2]
            self._chk_reverse.setChecked(True)
        else:
            self._chk_reverse.setChecked(False)

        index = self._cb_colormap.findText(colormap)
        if index is None:
            raise ValueError('Unknown colormap: %s' % colormap)
        self._cb_colormap.setCurrentIndex(index)

    def colorbarVisible(self):
        return self._chk_visible.isChecked()

    def setColorbarVisible(self, visible):
        self._chk_visible.setChecked(visible)

    def position(self):
        if self._rb_position.button(0).isChecked():
            return self.POSITION_INSIDE
        else:
            return self.POSITION_OUTSIDE

    def setPosition(self, position):
        if position == self.POSITION_INSIDE:
            self._rb_position.button(0).setChecked(True)
        elif position == self.POSITION_OUTSIDE:
            self._rb_position.button(1).setChecked(True)
        else:
            raise ValueError('Unknown position: %s' % position)

class _ColorbarDialog(QDialog):

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setWindowTitle('Color bar')

        # Widgets
        self._wdg_colorbar = ColorbarWidget()

        # FIXME: Implement colorbar position
        for button in self._wdg_colorbar._rb_position.buttons():
            button.setEnabled(False)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        # Layouts
        layout = QVBoxLayout()

        layout.addWidget(self._wdg_colorbar)
        layout.addWidget(buttons)

        self.setLayout(layout)

        # Signals
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

    def colormap(self):
        return self._wdg_colorbar.colormap()
        colormap = self._cb_colormap.currentText()
        if self._chk_reverse.isChecked():
            colormap += '_r'
        return colormap

    def setColormap(self, colormap):
        self._wdg_colorbar.setColormap(colormap)

    def colorbarVisible(self):
        return self._wdg_colorbar.colorbarVisible()

    def setColorbarVisible(self, visible):
        self._wdg_colorbar.setColorbarVisible(visible)

    def position(self):
        return self._wdg_colorbar.position()

    def setPosition(self, position):
        self._wdg_colorbar.setPosition(position)

class NavigationToolbarColorbarMixinQT(object):

    colorbar_changed = Signal(bool, str)

    def __init__(self):
        self._colorbar = None

    def _init_toolbar(self):
        a = QAction(getIcon('color-wheel'), 'Color bar', self)
        a.setToolTip('Change color bar')
        a.setEnabled(False)
        a.triggered.connect(self.colorbar)
        self._actions['colorbar'] = a
        self.insertAction(self._actions['configure_subplots'], a)

    def set_colorbar(self, colorbar):
        self._colorbar = colorbar
        self._actions['colorbar'].setEnabled(colorbar is not None)

    def get_colorbar(self):
        return self._colorbar

    def colorbar(self):
        cb = self.get_colorbar()

        dialog = _ColorbarDialog(self)
        dialog.setColorbarVisible(cb.ax.get_visible())
        dialog.setColormap(cb.mappable.get_cmap())
        if not dialog.exec_():
            return

        visible = dialog.colorbarVisible()
        cb.ax.set_visible(visible)

        cmap = dialog.colormap()
        cb.mappable.set_cmap(cmap)

        self.canvas.draw()

        cb = self.get_colorbar()
        cmap = cb.mappable.get_cmap()
        visible = cb.ax.get_visible()

        self.colorbar_changed.emit(visible, cmap.name)

class ScalebarWidget(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        # Widgets
        self._chk_visible = QCheckBox('Visible')

        self._cb_location = QComboBox()
        for text, index in sorted(ScaleBar._LOCATIONS.items(), key=itemgetter(1)):
            self._cb_location.addItem(text, index)

        self._sld_length_fraction = QSlider(Qt.Orientation.Horizontal)
        self._sld_length_fraction.setRange(0, 100)
        self._sld_length_fraction.setSingleStep(1)
        self._txt_length_fraction = QLabel()

        self._sld_height_fraction = QSlider(Qt.Orientation.Horizontal)
        self._sld_height_fraction.setRange(0, 100)
        self._sld_height_fraction.setSingleStep(1)
        self._txt_height_fraction = QLabel()

        self._cb_label_top = QComboBox()
        self._cb_label_top.addItem('Top', True)
        self._cb_label_top.addItem('Bottom', False)

        self._btn_color = ColorDialogButton()

        self._btn_box_color = ColorDialogButton()

        self._sld_box_alpha = QSlider(Qt.Orientation.Horizontal)
        self._sld_box_alpha.setRange(0, 100)
        self._sld_box_alpha.setSingleStep(1)
        self._txt_box_alpha = QLabel()

        # Layouts
        layout = QFormLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addRow(self._chk_visible)
        layout.addRow('Location', self._cb_location)
        layout.addRow("Length of scale bar\n(fraction of width)",
                      horizontal(self._sld_length_fraction,
                                 self._txt_length_fraction))
        layout.addRow("Height of scale bar\n(fraction of height)",
                      horizontal(self._sld_height_fraction,
                                 self._txt_height_fraction))
        layout.addRow('Label location', self._cb_label_top)
        layout.addRow("Text and scale color", self._btn_color)
        layout.addRow("Background color", self._btn_box_color)
        layout.addRow("Background alpha", horizontal(self._sld_box_alpha,
                                                     self._txt_box_alpha))

        self.setLayout(layout)

        # Signals
        self._sld_length_fraction.valueChanged.connect(self._on_length_fraction_changed)
        self._sld_height_fraction.valueChanged.connect(self._on_height_fraction_changed)
        self._sld_box_alpha.valueChanged.connect(self._on_box_alpha_changed)

        # Defaults
        self._sld_length_fraction.setValue(0)
        self._sld_height_fraction.setValue(0)
        self._sld_box_alpha.setValue(0)

    def _on_length_fraction_changed(self, value):
        self._txt_length_fraction.setText('%i%%' % value)

    def _on_height_fraction_changed(self, value):
        self._txt_height_fraction.setText('%i%%' % value)

    def _on_box_alpha_changed(self, value):
        self._txt_box_alpha.setText('%i%%' % value)

    def scalebarVisible(self):
        return self._chk_visible.isChecked()

    def setScalebarVisible(self, visible):
        self._chk_visible.setChecked(visible)

    def location(self):
        index = self._cb_location.currentIndex()
        return self._cb_location.itemData(index)

    def setLocation(self, location):
        index = self._cb_location.findData(location)
        self._cb_location.setCurrentIndex(index)

    def lengthFraction(self):
        return self._sld_length_fraction.value() / 100.0

    def setLengthFraction(self, fraction):
        self._sld_length_fraction.setValue(int(fraction * 100))

    def heightFraction(self):
        return self._sld_height_fraction.value() / 100.0

    def setHeightFraction(self, fraction):
        self._sld_height_fraction.setValue(int(fraction * 100))

    def labelTop(self):
        index = self._cb_label_top.currentIndex()
        return self._cb_label_top.itemData(index)

    def setLabelTop(self, label_top):
        index = self._cb_label_top.findData(label_top)
        self._cb_label_top.setCurrentIndex(index)

    def color(self):
        return self._btn_color.color()

    def setColor(self, color):
        self._btn_color.setColor(color)

    def boxColor(self):
        return self._btn_box_color.color()

    def setBoxColor(self, color):
        self._btn_box_color.setColor(color)

    def boxAlpha(self):
        return self._sld_box_alpha.value() / 100.0

    def setBoxAlpha(self, alpha):
        self._sld_box_alpha.setValue(int(alpha * 100))

class _ScalebarDialog(QDialog):

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setWindowTitle('Scale bar')

        # Widgets
        self._wdg_scalebar = ScalebarWidget()

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        # Layouts
        layout = QVBoxLayout()

        layout.addWidget(self._wdg_scalebar)
        layout.addWidget(buttons)

        self.setLayout(layout)

        # Signals
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

    def scalebarVisible(self):
        return self._wdg_scalebar.scalebarVisible()

    def setScalebarVisible(self, visible):
        self._wdg_scalebar.setScalebarVisible(visible)

    def location(self):
        return self._wdg_scalebar.location()

    def setLocation(self, location):
        self._wdg_scalebar.setLocation(location)

    def lengthFraction(self):
        return self._wdg_scalebar.lengthFraction()

    def setLengthFraction(self, fraction):
        self._wdg_scalebar.setLengthFraction(fraction)

    def heightFraction(self):
        return self._wdg_scalebar.heightFraction()

    def setHeightFraction(self, fraction):
        self._wdg_scalebar.setHeightFraction(fraction)

    def labelTop(self):
        return self._wdg_scalebar.labelTop()

    def setLabelTop(self, label_top):
        self._wdg_scalebar.setLabelTop(label_top)

    def color(self):
        return self._wdg_scalebar.color()

    def setColor(self, color):
        self._wdg_scalebar.setColor(color)

    def boxColor(self):
        return self._wdg_scalebar.boxColor()

    def setBoxColor(self, color):
        self._wdg_scalebar.setBoxColor(color)

    def boxAlpha(self):
        return self._wdg_scalebar.boxAlpha()

    def setBoxAlpha(self, fraction):
        self._wdg_scalebar.setBoxAlpha(fraction)

class NavigationToolbarScalebarMixinQT(object):

    scalebar_changed = Signal(bool, int, float, float, bool, tuple, tuple, float)

    def __init__(self):
        self._scalebar = None

    def _init_toolbar(self):
        a = QAction(getIcon('ruler'), 'Scale bar', self)
        a.setToolTip('Change scale bar')
        a.setEnabled(False)
        a.triggered.connect(self.scalebar)
        self._actions['scalebar'] = a
        self.insertAction(self._actions['configure_subplots'], a)

    def set_scalebar(self, scalebar):
        self._scalebar = scalebar
        self._actions['scalebar'].setEnabled(scalebar is not None)

    def get_scalebar(self):
        return self._scalebar

    def scalebar(self):
        sb = self.get_scalebar()

        dialog = _ScalebarDialog(self)
        dialog.setScalebarVisible(sb.get_visible())
        dialog.setLocation(sb.location)
        dialog.setLengthFraction(sb.length_fraction)
        dialog.setHeightFraction(sb.height_fraction)
        dialog.setLabelTop(sb.label_top)
        dialog.setColor(convert_color_mpl_to_qt(sb.color))
        dialog.setBoxColor(convert_color_mpl_to_qt(sb.box_color))
        dialog.setBoxAlpha(sb.box_alpha)
        if not dialog.exec_():
            return

        visible = dialog.scalebarVisible()
        location = dialog.location()
        length_fraction = dialog.lengthFraction()
        height_fraction = dialog.heightFraction()
        label_top = dialog.labelTop()
        color = convert_color_qt_to_mpl(dialog.color())
        box_color = convert_color_qt_to_mpl(dialog.boxColor())
        box_alpha = dialog.boxAlpha()

        sb.set_visible(visible)
        sb.location = location
        sb.length_fraction = length_fraction
        sb.height_fraction = height_fraction
        sb.label_top = label_top
        sb.color = color
        sb.box_color = box_color
        sb.box_alpha = box_alpha

        self.canvas.draw()

        self.scalebar_changed.emit(visible, location,
                                   length_fraction, height_fraction,
                                   label_top, color, box_color, box_alpha)

