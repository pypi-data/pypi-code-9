import os as _os
on_rtd = _os.environ.get('READTHEDOCS', None) == 'True'
if not on_rtd:
    import numpy as _np
    import matplotlib as mpl


class Rectangle(object):
    def __init__(self, x, y, width, height, axes=None, alpha=0.5, fill=True):
        self._axes = axes
        self._rect = mpl.patches.Rectangle((x, y), width, height, facecolor='w', edgecolor='r', alpha=alpha, fill=fill, axes=self._axes)

    @property
    def patch(self):
        return self._rect

    @property
    def _sorted_x(self):
        x_a = self._rect.get_x()
        x_b = x_a + self._rect.get_width()
        return _np.sort([x_a, x_b])

    @property
    def x0(self):
        """
        The smaller x coordinate.
        """
        return self._sorted_x[0]

    @property
    def x1(self):
        """
        The larger x coordinate.
        """
        return self._sorted_x[1]
    
    def get_x(self):
        return self.x0

    @property
    def _sorted_y(self):
        y_a = self._rect.get_y()
        y_b = y_a + self._rect.get_height()
        return _np.sort([y_a, y_b])

    @property
    def y0(self):
        """
        The smaller x coordinate.
        """
        return self._sorted_y[0]

    @property
    def y1(self):
        """
        The larger x coordinate.
        """
        return self._sorted_y[1]

    def get_y(self):
        return self.y0

    def get_xy(self):
        return (self.get_x(), self.get_y())

    def get_width(self):
        return self.x1-self.x0

    def get_height(self):
        return self.y1-self.y0

    def set_xy(self, value):
        return self._rect.set_xy(value)

    def set_width(self, value):
        return self._rect.set_width(value)

    def set_height(self, value):
        return self._rect.set_height(value)
