import os as _os
_on_rtd = _os.environ.get('READTHEDOCS', None) == 'True'
if not _on_rtd:
    import matplotlib.widgets as _mw
    import matplotlib.pyplot as _plt
    import matplotlib.patches as _mp

__all__ = ['RectangleSelector']


class RectangleSelector(object):
    """
    .. versionadded:: 1.2

    Add rectangle selection to an already-existing axis *as*. *\*args* and *\*\*kwargs* pass through to :class:`matplotlib.widgets.RectangleSelector`.

    Use key *A* or *a* to toggle whether the rectangle is active or not.

    *verbose* controls whether selections are printed to the terminal.
    """
    def __init__(self, ax, *args, selfunc=None, parent=None, verbose=False, **kwargs):
        # ======================================
        # Store things to class
        # ======================================
        self._parent          = parent
        self._selfunc         = selfunc
        self._ax              = ax
        self.verbose          = verbose
        self._selfunc_results = None
        self._x0 = 0
        self._x1 = 1
        self._y0 = 0
        self._y1 = 1

        # ======================================
        # Add rectangle selector
        # ======================================
        self._RectangleSelector = _mw.RectangleSelector(ax, self._onselect, *args, **kwargs)
        _plt.connect('key_press_event', self._toggle)

    def _onselect(self, eclick, erelease):
        # ======================================
        # Occurs on release
        # ======================================
        self._eclick = eclick
        self._erelease = erelease
        if self._verbose:
            print('eclick (x, y):\t\t({}, {})'.format(eclick.xdata, eclick.ydata))
            print('erelease (x, y):\t({}, {})'.format(erelease.xdata, erelease.ydata))

        self._x0 = min([self.erelease.xdata, self.eclick.xdata])
        self._x1 = max([self.erelease.xdata, self.eclick.xdata])
        self._y0 = min([self.erelease.ydata, self.eclick.ydata])
        self._y1 = max([self.erelease.ydata, self.eclick.ydata])

        self._set_rect()

        self._selfunc_results = self.selfunc(self)

    def _set_rect(self):
        try:
            self._rect.remove()
        except:
            pass

        self._rect = self._ax.add_patch(
            _mp.Rectangle(
                xy     = (self.x0, self.y0),
                width  = self.width,
                height = self.height,
                ec     = 'r',
                fc     = 'none'
                )
            )

        _plt.draw()


    def _toggle(self, event):
        if event.key in ['A', 'a']:
            self.RectangleSelector.set_active(not self.RectangleSelector.active)
        elif event.key in ['D', 'd']:
            try:
                self._rect.remove()
                _plt.draw()

                self._eclick          = None
                self._erelease        = None
                self._selfunc_results = None
            except:
                pass

    @property
    def parent(self):
        return self._parent

    @property
    def verbose(self):
        """
        Determines whether rectangle coordinates are printed to the terminal on selection.
        """
        return self._verbose

    @verbose.setter
    def verbose(self, value):
        self._verbose = value

    @property
    def RectangleSelector(self):
        """
        The instance of :class:`matplotlib.widgets.RectangleSelector`.
        """
        return self._RectangleSelector

    @property
    def ax(self):
        """
        The axis used.
        """
        return self._ax

    @property
    def selfunc(self):
        """
        A placeholder for the function called on each mouse release.
        """
        return self._selfunc

    @property
    def selfunc_results(self):
        """
        The results of :func:`selfunc(instance) <scisalt.matplotlib.RectangleSelector.selfunc>` where *instance* is this class.
        """
        if self.selfunc is not None:
            return self.selfunc(self)

    @property
    def eclick(self):
        """
        The starting mouse click from :class:`RectangleSelector <scisalt.matplotlib.RectangleSelector.RectangleSelector>`.
        """
        if self._eclick is None:
            raise IOError('No area was selected')
        else:
            return self._eclick

    @property
    def erelease(self):
        """
        The ending mouse click from :class:`RectangleSelector <scisalt.matplotlib.RectangleSelector.RectangleSelector>`.
        """
        if self._erelease is None:
            raise IOError('No area was selected')
        else:

            return self._erelease


    @property
    def x0(self):
        """
        Minimum x coordinate of rectangle.
        """
        return self._x0

    @x0.setter
    def x0(self, val):
        self._x0 = val
        self._set_rect()

    @property
    def x1(self):
        """
        Maximum x coordinate of rectangle.
        """
        return self._x1

    @x1.setter
    def x1(self, val):
        self._x1 = val
        self._set_rect()

    @property
    def y0(self):
        """
        Minimum y coordinate of rectangle.
        """
        return self._y0

    @y0.setter
    def y0(self, val):
        self._y0 = val
        self._set_rect()

    @property
    def y1(self):
        """
        Maximum y coordinate of rectangle.
        """
        return self._y1

    @y1.setter
    def y1(self, val):
        self._y1 = val
        self._set_rect()

    @property
    def xslice(self):
        return [self.x0, self.x1]

    @xslice.setter
    def xslice(self, val):
        self._x0, self._x1 = val
        self._set_rect()

    @property
    def yslice(self):
        return [self.y0, self.y1]

    @yslice.setter
    def yslice(self, val):
        self._y0, self._y1 = val
        self._set_rect()

    @property
    def width(self):
        """
        Width of rectangle.
        """
        return self.x1-self.x0

    @property
    def height(self):
        """
        Height of rectangle.
        """
        return self.y1-self.y0
