"""
Add scale bar to matplotlib's image 
"""

# Standard library modules.
import bisect
from operator import itemgetter

# Third party modules.
from matplotlib.artist import Artist
from matplotlib.cbook import is_string_like

from mpl_toolkits.axes_grid.anchored_artists import AnchoredSizeBar

# Local modules.
from pyhmsa.type.unit import _PREFIXES_VALUES

# Globals and constants variables.

class ScaleBar(Artist):

    zorder = 5

    _PREFERRED_VALUES = [1, 2, 5, 10, 15, 20, 25, 50, 75, 100, 125, 150, 200, 500, 750]

    _LOCATIONS = {'upper right':  1,
                  'upper left':   2,
                  'lower left':   3,
                  'lower right':  4,
                  'right':        5,
                  'center left':  6,
                  'center right': 7,
                  'lower center': 8,
                  'upper center': 9,
                  'center':       10,
              }

    def __init__(self, dx_m, length_fraction=0.2, height_fraction=0.01,
                 location=1, pad=0.2, border_pad=0.1, sep=5, frameon=True,
                 color='b', box_color='w', box_alpha=1.0,
                 label_top=False, font_properties=None,
                 **kwargs):
        """
        Creates a new scale bar.
        
        :arg dx_m: dimension of one pixel in meters (m)
        :arg length_fraction: length of the scale bar as a fraction of the 
            axes's width
        :arg height_fraction: height of the scale bar as a fraction of the 
            axes's height
        :arg location: a location code (same as legend)
        :arg pad: fraction of the legend font size
        :arg border_pad : fraction of the legend font size
        :arg sep : separation between scale bar and label in points
        :arg frameon : if True, will draw a box around the horizontal bar and label
        :arg color : color for the size bar and label
        :arg box_color: color of the box (if *frameon*)
        :arg box_alpha: transparency of box
        :arg label_top : if True, the label will be over the rectangle
        :arg font_properties: a matplotlib.font_manager.FontProperties instance, optional
            sets the font properties for the label text
        """
        Artist.__init__(self)

        self.dx_m = dx_m
        self.length_fraction = length_fraction
        self.height_fraction = height_fraction
        self.location = location
        self.pad = pad
        self.border_pad = border_pad
        self.sep = sep
        self.frameon = frameon
        self.color = color
        self.box_color = box_color
        self.box_alpha = box_alpha
        self.label_top = label_top
        self.font_properties = font_properties
        self._kwargs = kwargs

    def _calculate_length(self, length_px):
        length_m = length_px * self._dx_m

        prefixes_values = _PREFIXES_VALUES.copy()
        prefixes_values[''] = 1.0
        prefixes_values.pop('u')
        prefixes_values = sorted(prefixes_values.items(), key=itemgetter(1))
        values = [prefix_value[1] for prefix_value in prefixes_values]
        index = bisect.bisect_left(values, length_m)
        unit, factor = prefixes_values[index - 1]

        length_unit = length_m / factor
        index = bisect.bisect_left(self._PREFERRED_VALUES, length_unit)
        length_unit = self._PREFERRED_VALUES[index - 1]

        length_px = length_unit * factor / self._dx_m
        label = '%i %sm' % (length_unit, unit)

        return length_px, label

    def draw(self, renderer, *args, **kwargs):
        if not self.get_visible():
            return

        ax = self.get_axes()
        xlim, ylim = ax.get_xlim(), ax.get_ylim()

        length_px = abs(xlim[1] - xlim[0]) * self.length_fraction
        length_px, label = self._calculate_length(length_px)

        size_vertical = abs(ylim[1] - ylim[0]) * self.height_fraction

        sizebar = AnchoredSizeBar(transform=ax.transData,
                                  size=length_px,
                                  label=label,
                                  loc=self.location,
                                  pad=self.pad,
                                  borderpad=self.border_pad,
                                  sep=self.sep,
                                  frameon=self.frameon,
                                  size_vertical=size_vertical,
                                  color=self.color,
                                  label_top=self.label_top,
                                  fontproperties=self.font_properties,
                                  **self._kwargs)
        sizebar.set_axes(ax)
        sizebar.set_figure(self.get_figure())
        sizebar.patch.set_color(self.box_color)
        sizebar.patch.set_alpha(self.box_alpha)
        sizebar.draw(renderer)

    @property
    def dx_m(self):
        return self._dx_m

    @dx_m.setter
    def dx_m(self, dx_m):
        self._dx_m = float(dx_m)

    @property
    def length_fraction(self):
        return self._length_fraction

    @length_fraction.setter
    def length_fraction(self, fraction):
        assert 0.0 <= fraction <= 1.0
        self._length_fraction = float(fraction)

    @property
    def height_fraction(self):
        return self._height_fraction

    @height_fraction.setter
    def height_fraction(self, fraction):
        assert 0.0 <= fraction <= 1.0
        self._height_fraction = float(fraction)

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, loc):
        if is_string_like(loc):
            if loc not in self._LOCATIONS:
                raise ValueError('Unknown location code: %s' % loc)
            loc = self._LOCATIONS[loc]
        self._location = loc

    @property
    def pad(self):
        return self._pad

    @pad.setter
    def pad(self, pad):
        self._pad = float(pad)

    @property
    def border_pad(self):
        return self._border_pad

    @border_pad.setter
    def border_pad(self, pad):
        self._border_pad = float(pad)

    @property
    def sep(self):
        return self._sep

    @sep.setter
    def sep(self, sep):
        self._sep = float(sep)

    @property
    def frameon(self):
        return self._frameon

    @frameon.setter
    def frameon(self, on):
        self._frameon = bool(on)

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        self._color = color

    @property
    def box_color(self):
        return self._box_color

    @box_color.setter
    def box_color(self, color):
        self._box_color = color

    @property
    def box_alpha(self):
        return self._box_alpha

    @box_alpha.setter
    def box_alpha(self, alpha):
        assert 0.0 <= alpha <= 1.0
        self._box_alpha = alpha

    @property
    def label_top(self):
        return self._label_top

    @label_top.setter
    def label_top(self, top):
        self._label_top = bool(top)

    @property
    def font_properties(self):
        return self._font_properties

    @font_properties.setter
    def font_properties(self, props):
        self._font_properties = props

