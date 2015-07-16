# import matplotlib.pyplot as _plt

import os as _os
on_rtd = _os.environ.get('READTHEDOCS', None) == 'True'
if not on_rtd:
    import matplotlib.widgets as _wdg
    import numpy as _np

from .setup_figure import setup_figure   # noqa


class Imshow_Slider(object):
    """
    .. versionchanged:: 1.1.2
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
        self._AxesImage = self.ax.imshow(self._image, **kwargs)

        # ======================================
        # Add minimum slider
        # ======================================
        self.minslider = _wdg.Slider(self.ax_min, 'Min', self.imgmin, self.imgmax, minslide)

        # ======================================
        # Add maximum slider
        # ======================================
        self.maxslider = _wdg.Slider(self.ax_max, 'Max', self.imgmin, self.imgmax, maxslide, slidermin=self.minslider)
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
        return _np.max(self._image)

    # ======================================
    # Get max of image
    # ======================================
    @property
    def imgmin(self):
        """
        Lowest value of input image.
        """
        return _np.min(self._image)

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
