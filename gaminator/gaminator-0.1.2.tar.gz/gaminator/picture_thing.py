# -*- coding: utf-8 -*-


from .thing import Thing
from .canvas import Canvas
from .picture import Picture
from .exceptions import AssignmentUnsupported


class PictureThing(Thing):

    def _init_graphics(self):
        self.picture = Picture(20, 20)

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        raise AssignmentUnsupported()

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        raise AssignmentUnsupported()

    @property
    def picture(self):
        return self._picture

    @picture.setter
    def picture(self, picture):
        self._picture = picture
        self._canvas = Canvas(self._picture)
        self._width = picture.width
        self._height = picture.height

    @property
    def canvas(self):
        return self._canvas

    def _repaint(self, canvas):
        canvas.picture(
            self._picture,
            (self.border_left, self.border_up),
        )

    def paint(self, canvas):
        pass
