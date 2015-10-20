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
from .colorbar import colorbar

import pdb as pdb


class Imshow_Slider_Array(object):
    """
    .. versionchanged:: 1.5
       Name changed, colorbar options added, *p* changed to :class:`AxesImage <scisalt.matplotlib.Imshow_Slider.AxesImage>`.

    Convenience class for viewing images.
    
    Plots *image* to a to an instance of :class:`matplotlib.axis.imshow(**kwargs)`, with sliders for controlling bounds, with *\*\*kwargs* passed through to :meth:`matplotlib.axes.Axes.imshow`.

    *usecbar* determines if a colorbar will be used. Color bars can slow down the viewer significantly.
    """
    def __init__(self, images, usecbar=False, **kwargs):
        # ======================================
        # Save input info
        # ======================================
        self._images    = images
        self._num_imgs  = len(images)
        self._image_ind = 0
        self._kwargs    = kwargs
        self._usecbar   = usecbar

        # ======================================
        # Create figure
        # ======================================
        # self.fig, self.gs = setup_figure(20, 10, figsize=scaled_figsize(self.image))
        self.fig, self.gs = setup_figure(20, 10)
        self._ax_img = self.fig.add_subplot(self.gs[0:-4, :])
        self.ax_min = self.fig.add_subplot(self.gs[-3, 1:-1])
        self.ax_max = self.fig.add_subplot(self.gs[-2, 1:-1])
        self.ax_img = self.fig.add_subplot(self.gs[-1, 1:-1])

        self._reset(**kwargs)

        _plt.connect('key_press_event', self._keypress)

    def _keypress(self, event):
        self._event = event
        newval = None
        if event.key == 'right':
            newval = self.imageslider.val + 1
            if newval > self.num_imgs:
                newval = self.num_imgs
        elif event.key == 'left':
            newval = self.imageslider.val - 1
            if newval < 0:
                newval = 0

        if newval is not None:
            self.imageslider.set_val(newval)

        # if event.key in ['A', 'a']:
        #     self.RectangleSelector.set_active(not self.RectangleSelector.active)
        # elif event.key in ['D', 'd']:
        #     try:
        #         self._rect.remove()
        #         _plt.draw()

        #         self._eclick          = None
        #         self._erelease        = None
        #         self._selfunc_results = None
        #     except:
        #         pass

    def _fix_axes(self):
        shape_x, shape_y = self.image.shape
        ratio = shape_x / shape_y
        figsize = self._kwargs.get('figsize', _mpl.rcParams['figure.figsize'])
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

    def _reset(self, **kwargs):
        # ======================================
        # Strip kwargs for vmin, vmax
        # in order to set sliders correctly
        # ======================================
        minslide = kwargs.get('vmin', self.imgmin)
        maxslide = kwargs.get('vmax', self.imgmax)

        # ======================================
        # Slider Logic
        # ======================================
        if self.imgmin > 0:
            slidermin = kwargs.pop('smin', 0)
        else:
            slidermin = kwargs.pop('smin', self.imgmin)

        if self.imgmax < 0:
            slidermax = kwargs.pop('smax', 0)
        else:
            slidermax = kwargs.pop('smax', self.imgmax)

        # ======================================
        # Imshow
        # ======================================
        # self._AxesImage = self.ax.imshow(self.image, **kwargs)
        self._AxesImage = imshow(self.image, ax=self.ax, add_cbar=False, **kwargs)
        self._cax, self._cb = colorbar(self.ax, self._AxesImage)
        
        self._fix_axes()

        # ======================================
        # Add minimum slider
        # ======================================
        self.minslider = _wdg.Slider(self.ax_min, 'Min', slidermin, slidermax, minslide)

        # ======================================
        # Add maximum slider
        # ======================================
        self.maxslider = _wdg.Slider(self.ax_max, 'Max', slidermin, slidermax, maxslide, slidermin=self.minslider)
        self.minslider.slidermax = self.maxslider

        self.minslider.on_changed(self._update_clim)
        self.maxslider.on_changed(self._update_clim)

        # ======================================
        # Add image slider
        # ======================================
        self.imageslider = _wdg.Slider(ax=self.ax_img, label='Image', valmin=1, valmax=self.num_imgs, valinit=0, valfmt=u'%d')
        self.imageslider.on_changed(self._update_image)

        # if self.usecbar:
        #     self.fig.colorbar(self.AxesImage, ax=self.ax, use_gridspec=True)

        # self.fig.tight_layout()

    def _update_image(self, value):
        ind = _np.int(_np.round(value)-1)
        self._image_ind = ind

        # ======================================
        # Get old axes settings
        # ======================================
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()

        # ======================================
        # Clear old axes
        # ======================================
        self.ax.cla()
        self._cax.cla()

        # ======================================
        # Plot new data
        # ======================================
        self._AxesImage = imshow(self.image, ax=self.ax, add_cbar=False, **self._kwargs)
        self._cb = _plt.colorbar(self._AxesImage, cax=self._cax)

        # ======================================
        # Fix the axes
        # ======================================
        self._fix_axes()

        # ======================================
        # Keep the colorbar to previous settings
        # ======================================
        self._update_clim(0)

        # ======================================
        # Get old axes settings
        # ======================================
        self.ax.set_xlim(xlim)
        self.ax.set_ylim(ylim)

        
    def set_cmap(self, cmap):
        """
        Sets color map to *cmap*.
        """
        self.AxesImage.set_cmap(cmap)

    @property
    def num_imgs(self):
        return self._num_imgs

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
    # Get max of image
    # ======================================
    @property
    def imgmax(self):
        """
        Highest value of input image.
        """
        if not hasattr(self, '_imgmax'):
            imgmax = _np.max(self.images[0])
            for img in self.images:
                imax = _np.max(img)
                if imax > imgmax:
                    imgmax = imax

            self._imgmax = imgmax

        return self._imgmax

    # ======================================
    # Get min of image
    # ======================================
    @property
    def imgmin(self):
        """
        Lowest value of input image.
        """
        if not hasattr(self, '_imgmin'):
            imgmin = _np.min(self.images[0])
            for img in self.images:
                imin = _np.min(img)
                if imin > imgmin:
                    imgmin = imin

            self._imgmin = imgmin
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
    def images(self):
        """
        The array of images.
        """
        return self._images

    @property
    def image(self):
        """
        The image loaded.
        """
        return self._images[self._image_ind]
