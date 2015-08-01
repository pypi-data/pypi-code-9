# import matplotlib.pyplot as _plt

import os as _os
on_rtd = _os.environ.get('READTHEDOCS', None) == 'True'
if not on_rtd:
    import matplotlib.widgets as _wdg
    import matplotlib as _mpl
    import numpy as _np
    import matplotlib.pyplot as _plt

from .setup_figure import setup_figure   # noqa
from .imshow import imshow
from .imshow import scaled_figsize


class Imshow_Slider(object):
    """
    .. versionchanged:: 1.2
       Name changed, colorbar options added, *p* changed to :class:`AxesImage <scisalt.matplotlib.Imshow_Slider.AxesImage>`.

    Convenience class for viewing images.
    
    Plots *image* to a to an instance of :class:`matplotlib.axis.imshow(**kwargs)`, with sliders for controlling bounds, with *\*\*kwargs* passed through to :meth:`matplotlib.axes.Axes.imshow`.

    *usecbar* determines if a colorbar will be used. Color bars can slow down the viewer significantly.
    """
    def __init__(self, image, usecbar=False, **kwargs):
        # ======================================
        # Save input info
        # ======================================
        self._image  = image
        self._kwargs = kwargs
        self.usecbar = usecbar

        # ======================================
        # Create figure
        # ======================================
        # self.fig, self.gs = setup_figure(20, 10, figsize=scaled_figsize(self.image))
        self.fig, self.gs = setup_figure(20, 10)
        self._ax_img = self.fig.add_subplot(self.gs[0:-3, :])
        self.ax_min = self.fig.add_subplot(self.gs[-2, 1:-1])
        self.ax_max = self.fig.add_subplot(self.gs[-1, 1:-1])

        self._reset(**kwargs)

    def _reset(self, **kwargs):
        # ======================================
        # Strip kwargs for vmin, vmax
        # in order to set sliders correctly
        # ======================================
        minslide = kwargs.get('vmin', self.imgmin)
        maxslide = kwargs.get('vmax', self.imgmax)

        # ======================================
        # Imshow
        # ======================================
        # self._AxesImage = self.ax.imshow(self.image, **kwargs)
        self._AxesImage = imshow(self.image, ax=self.ax, **kwargs)
        
        shape_x, shape_y = self.image.shape
        ratio = shape_x / shape_y
        figsize = kwargs.get('figsize', _mpl.rcParams['figure.figsize'])
        figsize_ratio = figsize[0]/figsize[1]
        if ratio > figsize_ratio:
            x_lim = [0, shape_x]
            y_lim = shape_x / figsize_ratio
            y_lim = [(shape_y-y_lim)/2, (shape_y+y_lim)/2]
        else:
            x_lim = shape_y * figsize_ratio
            x_lim = [(shape_x-x_lim)/2, (shape_x+x_lim)/2]
            y_lim = [0, shape_y]

        self.ax.set_xlim(x_lim)
        self.ax.set_ylim(y_lim)

        # ======================================
        # Add minimum slider
        # ======================================
        # self.minslider = _wdg.Slider(self.ax_min, 'Min', self.imgmin, self.imgmax, minslide)
        self.minslider = _wdg.Slider(self.ax_min, 'Min', 0, self.imgmax, minslide)

        # ======================================
        # Add maximum slider
        # ======================================
        # self.maxslider = _wdg.Slider(self.ax_max, 'Max', self.imgmin, self.imgmax, maxslide, slidermin=self.minslider)
        self.maxslider = _wdg.Slider(self.ax_max, 'Max', 0, self.imgmax, maxslide, slidermin=self.minslider)
        self.minslider.slidermax = self.maxslider

        self.minslider.on_changed(self._update_clim)
        self.maxslider.on_changed(self._update_clim)

        if self.usecbar:
            self.fig.colorbar(self.AxesImage, ax=self.ax, use_gridspec=True)

        self.fig.tight_layout()

    def set_cmap(self, cmap):
        """
        Sets color map to *cmap*.
        """
        self.AxesImage.set_cmap(cmap)

    @property
    def AxesImage(self):
        """
        The :class:`matplotlib.image.AxesImage` from :meth:`matplotlib.axes.Axes.imshow`.
        """
        return self._AxesImage

    @property
    def ax(self):
        """
        The :class:`matplotlib.axes.Axes` used for :meth:`matplotlib.axes.Axes.imshow`.
        """
        return self._ax_img

    # ======================================
    # Get min of image
    # ======================================
    @property
    def imgmax(self):
        """
        Highest value of input image.
        """
        return _np.max(self.image)

    # ======================================
    # Get max of image
    # ======================================
    @property
    def imgmin(self):
        """
        Lowest value of input image.
        """
        return _np.min(self.image)

    # ======================================
    # Update the clims
    # ======================================
    def _update_clim(self, val):
        cmin = self.minslider.val
        cmax = self.maxslider.val
        # print('Cmin: {}, Cmax: {}'.format(cmin, cmax))
        self.AxesImage.set_clim(cmin, cmax)

    # ======================================
    # Easily get and set slider
    # ======================================
    @property
    def clim_min(self):
        """
        Slider value for minimum
        """
        return self.minslider.val

    @clim_min.setter
    def clim_min(self, val):
        self.minslider.set_val(val)

    @property
    def clim_max(self):
        """
        Slider value for maximum
        """
        return self.maxslider.val

    @clim_max.setter
    def clim_max(self, val):
        self.maxslider.set_val(val)

    @property
    def image(self):
        """
        The image loaded.
        """
        return self._image
