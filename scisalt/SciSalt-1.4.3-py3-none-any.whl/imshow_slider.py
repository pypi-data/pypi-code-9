# import matplotlib.pyplot as _plt

from .setup_figure import setup_figure   # noqa
import matplotlib.widgets as _wdg
import numpy as _np
import ipdb                              # noqa


class imshow_slider(object):
    def __init__(self, image, **kwargs):
        # ======================================
        # Save input info
        # ======================================
        self._image  = image
        self._kwargs = kwargs

        # ======================================
        # Create figure
        # ======================================
        self.fig, self.gs = setup_figure(20, 10)
        self.ax_img = self.fig.add_subplot(self.gs[0:-3, :])
        self.ax_min = self.fig.add_subplot(self.gs[-2, 1:-1])
        self.ax_max = self.fig.add_subplot(self.gs[-1, 1:-1])

        self._reset(**kwargs)

    def _reset(self, **kwargs):
        # ======================================
        # Imshow
        # ======================================
        self.p = self.ax_img.imshow(self._image, **kwargs)
        self.p.set_cmap('jet')

        # ======================================
        # Add minimum slider
        # ======================================
        self.minslider = _wdg.Slider(self.ax_min, 'Min', self.imgmin, self.imgmax, self.imgmin)

        # ======================================
        # Add maximum slider
        # ======================================
        self.maxslider = _wdg.Slider(self.ax_max, 'Max', self.imgmin, self.imgmax, self.imgmax, slidermin=self.minslider)
        self.minslider.slidermax = self.maxslider

        self.minslider.on_changed(self._update_clim)
        self.maxslider.on_changed(self._update_clim)

        self.fig.tight_layout()

    # ======================================
    # Get min of image
    # ======================================
    @property
    def imgmax(self):
        return _np.max(self._image)

    # ======================================
    # Get max of image
    # ======================================
    @property
    def imgmin(self):
        return _np.min(self._image)

    # ======================================
    # Update the clims
    # ======================================
    def _update_clim(self, val):
        cmin = self.minslider.val
        cmax = self.maxslider.val
        # print('Cmin: {}, Cmax: {}'.format(cmin, cmax))
        self.p.set_clim(cmin, cmax)

    # ======================================
    # Easily get and set slider
    # ======================================
    @property
    def clim_min(self):
        return self.minslider.val

    @clim_min.setter
    def clim_min(self, val):
        self.minslider.set_val(val)

    @property
    def clim_max(self):
        return self.maxslider.val

    @clim_max.setter
    def clim_max(self, val):
        self.maxslider.set_val(val)
