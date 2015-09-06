# -*- coding: utf-8 -*-


from .thing_type import _ThingType
from .picture import Obrazok
from .canvas import Platno


# Python 2 and 3 compatible way to define metaclass
def _with_metaclass(mcls):
    def decorator(cls):
        body = vars(cls).copy()
        body.pop('__dict__', None)
        body.pop('__weakref__', None)
        return mcls(cls.__name__, cls.__bases__, body)
    return decorator


@_with_metaclass(_ThingType)
class Vec(object):

    _next_id = 1

    def __init__(self, **kwargs):
        self._world = None

        self.id = Vec._next_id
        Vec._next_id += 1

        self.x = 0
        self.y = 0
        self._z = 0
        self.x_zarovnanie = 0.5
        self.y_zarovnanie = 0.5

        self._init_graphics()

        for key in kwargs:
            setattr(self, key, kwargs[key])

        calls = []

        for cls in self.__class__.mro():
            if isinstance(cls, _ThingType):
                for fname in cls._gaminator_events['NASTAV']:
                    calls.append(getattr(self, fname))

        for f in calls:
            f()

    def _init_graphics(self):
        self._width = 20
        self._height = 20
        self._will_repaint = True
        self._will_resize = True
        self._picture = Obrazok(20, 20)

    @property
    def svet(self):
        return self._world

    @svet.setter
    def svet(self, value):
        if self._world is not None:
            self._world._disconnect_thing(self)
        if value is not None:
            value._connect_thing(self)
        self._world = value

    @svet.deleter
    def svet(self):
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
    def sirka(self):
        return self._width

    @sirka.setter
    def sirka(self, sirka):
        self._will_resize = True
        self._width = sirka

    @property
    def vyska(self):
        return self._height

    @vyska.setter
    def vyska(self, vyska):
        self._will_resize = True
        self._height = vyska

    @property
    def okraj_vlavo(self):
        return self.x + (0-self.x_zarovnanie)*self._width

    @property
    def okraj_vpravo(self):
        return self.x + (1-self.x_zarovnanie)*self._width

    @property
    def okraj_hore(self):
        return self.y + (0-self.y_zarovnanie)*self._height

    @property
    def okraj_dole(self):
        return self.y + (1-self.y_zarovnanie)*self._height

    def prekryva_sa(self, druhy):
        return (
            max(
                self.okraj_vlavo,
                druhy.okraj_vlavo,
            ) < min(
                self.okraj_vpravo,
                druhy.okraj_vpravo,
            ) and max(
                self.okraj_hore,
                druhy.okraj_hore,
            ) < min(
                self.okraj_dole,
                druhy.okraj_dole,
            )
        )

    def prekresli(self):
        self._will_repaint = True

    def _repaint(self, canvas):
        if self._will_resize:
            self._will_repaint = True
            self._picture.zresetuj(
                sirka=self._width, vyska=self._height,
            )
            self._will_resize = False
        if self._will_repaint:
            self._picture.zmaz()
            self.vykresli(Platno(self._picture))
            self._will_repaint = False
        canvas.obrazok(
            self._picture,
            (self.okraj_vlavo, self.okraj_hore),
        )

    def setup(self, *args, **kwargs):
        pass

    def step(self):
        pass

    def vykresli(self, platno):
        pass
