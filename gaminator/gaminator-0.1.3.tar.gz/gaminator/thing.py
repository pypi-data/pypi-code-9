# -*- coding: utf-8 -*-


from .thing_type import _ThingType
from .picture import Picture
from .canvas import Canvas


# Python 2 and 3 compatible way to define metaclass
def _with_metaclass(mcls):
    def decorator(cls):
        body = vars(cls).copy()
        body.pop('__dict__', None)
        body.pop('__weakref__', None)
        return mcls(cls.__name__, cls.__bases__, body)
    return decorator


@_with_metaclass(_ThingType)
class Thing(object):

    _next_id = 1

    def __init__(self, **kwargs):
        self._world = None

        self.id = Thing._next_id
        Thing._next_id += 1

        self.x = 0
        self.y = 0
        self._z = 0
        self.x_align = 0.5
        self.y_align = 0.5

        self._init_graphics()

        for key in kwargs:
            setattr(self, key, kwargs[key])

        calls = []

        for cls in self.__class__.mro():
            if isinstance(cls, _ThingType):
                for fname in cls._gaminator_events['SETUP']:
                    calls.append(getattr(self, fname))

        for f in calls:
            f()

    def _init_graphics(self):
        self._width = 20
        self._height = 20
        self._will_repaint = True
        self._will_resize = True
        self._picture = Picture(20, 20)

    @property
    def world(self):
        return self._world

    @world.setter
    def world(self, value):
        if self._world is not None:
            self._world._disconnect_thing(self)
        if value is not None:
            value._connect_thing(self)
        self._world = value

    @world.deleter
    def world(self):
        if self._world is not None:
            self._world._disconnect_thing(self)
        self._world = None

    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, z):
        self._z = z
        if self._world is not None:
            self._world._recalculate_z = True

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, width):
        self._will_resize = True
        self._width = width

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, height):
        self._will_resize = True
        self._height = height

    @property
    def border_left(self):
        return self.x + (0-self.x_align)*self._width

    @property
    def border_right(self):
        return self.x + (1-self.x_align)*self._width

    @property
    def border_up(self):
        return self.y + (0-self.y_align)*self._height

    @property
    def border_down(self):
        return self.y + (1-self.y_align)*self._height

    def collides(self, other):
        return (
            max(
                self.border_left,
                other.border_left,
            ) < min(
                self.border_right,
                other.border_right,
            ) and max(
                self.border_up,
                other.border_up,
            ) < min(
                self.border_down,
                other.border_down,
            )
        )

    def repaint(self):
        self._will_repaint = True

    def _repaint(self, canvas):
        if self._will_resize:
            self._will_repaint = True
            self._picture.reset(
                width=self._width, height=self._height,
            )
            self._will_resize = False
        if self._will_repaint:
            self._picture.clear()
            self.paint(Canvas(self._picture))
            self._will_repaint = False
        canvas.picture(
            self._picture,
            (self.border_left, self.border_up),
        )

    def setup(self, *args, **kwargs):
        pass

    def step(self):
        pass

    def paint(self, canvas):
        pass
