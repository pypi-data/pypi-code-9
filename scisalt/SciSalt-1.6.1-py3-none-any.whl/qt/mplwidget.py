from PyQt4 import QtGui
from PyQt4 import QtCore
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as _FigureCanvas
from matplotlib.backends.backend_qt4 import NavigationToolbar2QT as _NavigationToolbar
import matplotlib as _mpl
import numpy as _np

from .Rectangle import Rectangle

import pdb
import traceback

import logging
loggerlevel = logging.DEBUG
logger = logging.getLogger(__name__)

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class Slider_and_Text(QtGui.QWidget):
    valueChanged = QtCore.pyqtSignal(int)
    sliderReleased = QtCore.pyqtSignal(int)

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self)
        self.setMaximumHeight(40)
        # Enable tracking by default
        self._tracking = True
        self.hLayout   = QtGui.QHBoxLayout()
        self.slider    = QtGui.QSlider()

        self.leftbutton = QtGui.QPushButton()
        self.leftbutton.setText("<")
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.leftbutton.sizePolicy().hasHeightForWidth())
        #  self.leftbutton.setSizePolicy(sizePolicy)
        self.leftbutton.clicked.connect(self._subone)

        self.rightbutton = QtGui.QPushButton()
        self.rightbutton.setText(">")
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rightbutton.sizePolicy().hasHeightForWidth())
        #  self.rightbutton.setSizePolicy(sizePolicy)
        self.rightbutton.clicked.connect(self._addone)

        self.v = QtGui.QIntValidator()
        self.box = QtGui.QLineEdit()
        self.box.setValidator(self.v)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.box.sizePolicy().hasHeightForWidth())
        #  self.box.setSizePolicy(sizePolicy)

        self.hLayout.addWidget(self.leftbutton)
        self.hLayout.addWidget(self.slider)
        self.hLayout.addWidget(self.box)
        self.hLayout.addWidget(self.rightbutton)
        self.setLayout(self.hLayout)
        
        self.slider.valueChanged.connect(self._sliderChanged)
        self.box.editingFinished.connect(self._textChanged)
        self.setOrientation(QtCore.Qt.Horizontal)

        # Connect release so tracking works as expected
        self.slider.sliderReleased.connect(self._sliderReleased)

    def _addone(self):
        self.value = self.value + 1
        self.valueChanged.emit(self.value)

    def _subone(self):
        self.value = self.value - 1
        self.valueChanged.emit(self.value)

    def _sliderReleased(self):
        print('Released')
        self.sliderReleased.emit(self.slider.value)

    def setTracking(self, val):
        print('Tracking set to {}'.format(val))
        self._tracking = val

    def setMaximum(self, val):
        self.slider.setMaximum(val)
        self.v.setRange(self.slider.minimum(), self.slider.maximum())
        self.box.setValidator(self.v)

    def setMinimum(self, val):
        self.slider.setMinimum(val)
        self.v.setRange(self.slider.minimum(), self.slider.maximum())
        self.box.setValidator(self.v)

    def _sliderChanged(self, val):
        self.box.setText(str(val))
        if self._tracking:
            try:
                self.slider.sliderReleased.disconnect()
            except:
                pass
            self.valueChanged.emit(val)
        else:
            try:
                self.slider.sliderReleased.disconnect()
            except:
                pass
            self.slider.sliderReleased.connect(self._sliderChanged_notracking)

    def _sliderChanged_notracking(self):
        val = self.slider.value()
        # print('Value to be emitted is {}'.format(val))
        self.valueChanged.emit(val)

    def _textChanged(self):
        val = self.box.text()
        self.slider.setValue(int(val))
        self._sliderChanged_notracking()

    def setOrientation(self, *args, **kwargs):
        self.slider.setOrientation(*args, **kwargs)

    def _getValue(self):
        return self.slider.value()

    def _setValue(self, val):
        self.slider.setValue(val)
        self.box.setText(str(val))
    value = property(_getValue, _setValue)

    def setValue(self, val):
        self.slider.setValue(val)
        self.box.setText(str(val))
        # self.valueChanged.emit(val)


class Mpl_Plot(_FigureCanvas):
    def __init__(self, parent=None):
        # Initialize things
        self.fig = _mpl.figure.Figure()
        _FigureCanvas.__init__(self, self.fig)
        _FigureCanvas.setSizePolicy(self, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        _FigureCanvas.updateGeometry(self)

        # Create axes
        self.ax = self.fig.add_subplot(111)

    def plot(self, *args, **kwargs):
        self.ax.clear()
        self.ax.plot(*args, **kwargs)
        self.ax.ticklabel_format(style='sci', scilimits=(0, 0), axis='y')
        self.ax.figure.canvas.draw()


class Mpl_Image(QtGui.QWidget):
    # Signal for when the rectangle is changed
    rectChanged = QtCore.pyqtSignal(Rectangle)

    def __init__(self, parent=None, rectbool = True, toolbarbool=False, image=None):
        # Initialize things
        QtGui.QWidget.__init__(self)
        self.rectbool  = rectbool
        self._clim_min = 0
        self._clim_max = 3600

        self._pressed = False

        # Add a vertical layout
        self.vLayout = QtGui.QVBoxLayout()

        # Add a figure
        self.fig = _mpl.figure.Figure()

        # Add a canvas containing the fig
        self.canvas = _FigureCanvas(self.fig)
        _FigureCanvas.setSizePolicy(self.canvas, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        _FigureCanvas.updateGeometry(self.canvas)

        # Setup the layout
        if toolbarbool:
            self.toolbar = _NavigationToolbar(self.canvas, self)
            self.toolbar.setMaximumHeight(20)
            self.vLayout.addWidget(self.toolbar)
        self.vLayout.addWidget(self.canvas)
        self.setLayout(self.vLayout)

        # Create axes
        self.ax = self.fig.add_subplot(111)

        # Include rectangle functionality
        if rectbool:
            self.fig.canvas.mpl_connect('button_press_event', self.on_press)
            self.fig.canvas.mpl_connect('button_release_event', self.on_release)
            self.Rectangle = Rectangle(
                x      = -10     ,
                y      = 0       ,
                width  = 0       ,
                height = 3       ,
                axes   = self.ax
                )

        # Add image
        self.image = image

    def _get_img(self):
        return self._image

    def _set_img(self, image):
        self.ax.clear()
        self._image = image
        if image is not None:
            self._imgplot = self.ax.imshow(image, interpolation='none')
            if self.rectbool:
                self.ax.add_patch(self.Rectangle.get_rect())
            # imagemax = _np.max(_np.max(image))
            self.set_clim(self._clim_min, self._clim_max)
    image = property(_get_img, _set_img)

    def set_clim(self, clim_min, clim_max):
        if self.image is not None:
            self._clim_min = clim_min
            self._clim_max = clim_max
            self._imgplot.set_clim(clim_min, clim_max)
            self.ax.figure.canvas.draw()

    def on_press(self, event):
        if self.toolbar._active is None:
            self._pressed = True
            self.x0 = event.xdata
            self.y0 = event.ydata
            logger.log(level=loggerlevel, msg='Pressed: x0: {}, y0: {}'.format(self.x0, self.y0))

    def on_release(self, event):
        if self._pressed:
            self._pressed = False
            print('release')
            self.x1 = event.xdata
            self.y1 = event.ydata
            width   = self.x1 - self.x0
            height  = self.y1 - self.y0

            logger.log(level=loggerlevel, msg='Released: x0: {}, y0: {}, x1: {}, y1: {}, width: {}, height: {}'.format(
                self.x0 ,
                self.y0 ,
                self.x1 ,
                self.y1 ,
                width   ,
                height
                )
                )

            self.Rectangle.set_xy((self.x0, self.y0))
            self.Rectangle.set_width(width)
            self.Rectangle.set_height(height)
            self.ax.figure.canvas.draw()

            self.rectChanged.emit(self.Rectangle)
            # print(self.rect)

    def zoom_rect(self, border=None, border_px=None):
        # ======================================
        # Get x coordinates
        # ======================================
        x0 = self.Rectangle.get_x()
        width = self.Rectangle.get_width()
        x1 = x0+width

        # ======================================
        # Get y coordinates
        # ======================================
        y0 = self.Rectangle.get_y()
        height = self.Rectangle.get_height()
        y1 = y0+height

        # ======================================
        # Validate borders
        # ======================================
        if (border_px is None) and (border is not None):
            xborder = border[0]*width
            yborder = border[1]*height
        elif (border_px is not None) and (border is None):
            xborder = border_px[0]
            yborder = border_px[1]
        elif (border_px is None) and (border is None):
            raise IOError('No border info specified!')
        elif (border_px is not None) and (border is not None):
            raise IOError('Too much border info specified, both border_px and border!')
        else:
            raise IOError('End of the line!')

        # ======================================
        # Add borders
        # ======================================
        x0 = x0 - xborder
        x1 = x1 + xborder
        y0 = y0 - yborder
        y1 = y1 + yborder

        # ======================================
        # Validate coordinates to prevent
        # unPythonic crash
        # ======================================
        if not ((0 <= x0 and x0 <= self.image.shape[1]) and (0 <= x1 and x1 <= self.image.shape[1])):
            print('X issue')
            print('Requested: x=({}, {})'.format(x0, x1))
            x0 = 0
            x1 = self.image.shape[1]
        if not ((0 <= y0 and y0 <= self.image.shape[0]) and (0 <= y1 and y1 <= self.image.shape[0])):
            print('y issue')
            print('Requested: y=({}, {})'.format(y0, y1))
            y0 = 0
            y1 = self.image.shape[0]

        # ======================================
        # Set viewable area
        # ======================================
        self.ax.set_xlim(x0, x1)
        self.ax.set_ylim(y0, y1)

        # ======================================
        # Redraw canvas to show updates
        # ======================================
        self.ax.figure.canvas.draw()


class Mpl_Image_Plus_Slider(QtGui.QWidget):
    # def __init__(self, parent=None, **kwargs):
    def __init__(self, parent=None, **kwargs):
        # Initialize self as a widget
        QtGui.QWidget.__init__(self, parent)

        # Add a vertical layout with parent self
        self.vLayout = QtGui.QVBoxLayout(self)
        self.vLayout.setObjectName(_fromUtf8("vLayout"))

        # Add an Mpl_Image widget to vLayout,
        # save it to self._img
        # Pass arguments through to Mpl_Image.
        self._img = Mpl_Image(parent=parent, toolbarbool=True, **kwargs)
        self._img.setObjectName(_fromUtf8("_img"))
        self.vLayout.addWidget(self._img)

        # Add a slider to vLayout,
        # save it to self.max_slider
        # self.max_slider = QtGui.QSlider(self)
        self.max_slider = Slider_and_Text(self)
        self.max_slider.setObjectName(_fromUtf8("max_slider"))
        self.max_slider.setOrientation(QtCore.Qt.Horizontal)
        self.vLayout.addWidget(self.max_slider)

        # Setup slider to work with _img's clims
        self.max_slider.valueChanged.connect(lambda val: self.set_clim(0, val))

    def _get_image(self):
        return self._img.image

    def _set_image(self, image):
        self._img.image = image
        maximage = _np.max(_np.max(image))
        self.max_slider.setMaximum(maximage)
    image = property(_get_image, _set_image)

    def _get_ax(self):
        return self._img.ax
    ax = property(_get_ax)

    def _get_Rectangle(self):
        return self._img.Rectangle
    #  def _set_rect(self, rect):
    #          self._img.rect(rect)
    Rectangle = property(_get_Rectangle)

    def zoom_rect(self, border=None, border_px=None):
        self._img.zoom_rect(border, border_px)

    def set_clim(self, *args, **kwargs):
        self._img.set_clim(*args, **kwargs)

    def setSliderValue(self, val):
        self.max_slider.setValue(val)
