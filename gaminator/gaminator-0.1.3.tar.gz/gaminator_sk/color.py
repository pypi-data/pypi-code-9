#  -*- coding: utf-8 -*-


from .constants import CONSTANTS


class Farba(object):

    def __init__(self, r, g, b, a=255):
        self._r = int(r)
        self._g = int(g)
        self._b = int(b)
        self._a = int(a)

        # @HACK: Internal colorkey
        if r == 0 and g == 1 and b == 0:
            self._g = 0

    @property
    def r(self):
        return self._r

    @property
    def g(self):
        return self._g

    @property
    def b(self):
        return self._b

    @property
    def a(self):
        return self._a

    def _tuple(self):
        return (
            max(min(self._r, 255), 0),
            max(min(self._g, 255), 0),
            max(min(self._b, 255), 0),
            max(min(self._a, 255), 0)
        )

    def __len__(self):
        return 4

    def __getitem__(self, index):
        return self._tuple()[index]

    def __mul__(self, other):
        return Farba(
            self._r * other, self._g * other, self._b * other, self._a * other
        )

    def __add__(self, other):
        return Farba(
            self._r + other._r, self._g + other._g,
            self._b + other._b, self._a + other._a
        )

    def __rmul__(self, other):
        return self * other

    def upravena(self, r=None, g=None, b=None, a=None):
        return Farba(
            r if r is not None else self._r, g if g is not None else self._g,
            b if b is not None else self._b, a if a is not None else self._a,
        )

    def zmiesana(self, druhy, pomer=0.5):
        return self * pomer + druhy * (1 - pomer)


CONSTANTS['CIERNA'] = Farba(0, 0, 0)
CONSTANTS['BIELA'] = Farba(255, 255, 255)
CONSTANTS['MODRA'] = Farba(0, 0, 255)
CONSTANTS['ZELENA'] = Farba(0, 255, 0)
CONSTANTS['CERVENA'] = Farba(255, 0, 0)
CONSTANTS['ZLTA'] = Farba(255, 255, 0)
