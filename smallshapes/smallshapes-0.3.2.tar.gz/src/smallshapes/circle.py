# -*- coding: utf8 -*-

from math import pi, sqrt
from smallvectors import dot, Vec, Point
from smallvectors.core import FlatView
from smallshapes.base import ConvexAny, Convex, mConvex


SQRT_HALF = 1 / sqrt(2)

class CircleAny(ConvexAny):

    '''Any class for Circle and mCircle classes'''

    __slots__ = ['_radius', '_x', '_y']
    __flatview = FlatView

    def __init__(self, radius, pos=(0, 0)):
        self._radius = radius
        self._x, self._y = pos

    #
    # Abstract methods
    #
    def __len__(self):
        return 2
    
    def __iter__(self):
        yield self._radius
        yield Vec(self._x, self._y)

    def __repr__(self):
        fmt = type(self).__name__, self.radius, tuple(self.pos)
        return '%s(%s, pos=%s)' % fmt
    
    def displaced_by_vector_to(self, vec):
        return Circle(self.radius, self.pos + vec)
    
    @property
    def flat(self):
        return self.__flatview(self)

    @property
    def pos(self):
        return Vec(self._x, self._y)

    @property
    def center(self):
        return Point(self._x, self._y)

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def area(self):
        return pi * self._radius * self._radius

    def ROG_sqr(self):
        return self._radius * self._radius / 2

    def ROG(self):
        return self._radius * SQRT_HALF

    # Métodos utilizado pelo SAT ##############################################
    def directions(self, n):
        '''Retorna a lista de direções exaustivas para o teste do SAT
        associadas ao objeto.

        A rigor esta lista é infinita para um círculo. Retornamos uma lista
        vazia de forma que somente as direções do outro objeto serão
        consideradas'''

        return []

    def shadow(self, n):
        '''Retorna as coordenadas da sombra na direção n dada.
        Assume n normalizado.'''

        p0 = dot(self._pos, n)
        r = self._radius
        return (p0 - r, p0 + r)

    # Cálculo de distâncias ###################################################
    def distance_center(self, other):
        '''Retorna a distância entre centros de dois círculos.'''

        return self._pos.distance(other.pos)

    def distance_circle(self, other):
        '''Retorna a distância para um outro círculo. Zero se eles se
        interceptam'''

        distance = self._pos.distance(other.pos)
        sum_radius = self._radius + other.radius
        return max(distance - sum_radius, 0)

    # Containement FGAme_tests ###############################################
    def contains_circle(self, other):
        return (self.contains_point(other.pos) and
                (self.distance_center(other) + other.radius < self._radius))

    def contains_point(self, point):
        return self._pos.distance(point) <= self._radius


class Circle(CircleAny, Convex):

    '''Representa um círculo imutável.
    
    Examples
    --------
    
    >>> c1 = Circle(5)
    '''

    __slots__ = []

    @property
    def radius(self):
        return self._radius


class mCircle(CircleAny, mConvex):

    '''A mutable circle class'''

    __slots__ = []
    def __setitem_simple__(self, key, value):
        if key == 0:
            self._radius = value
        elif key == 1:
            self._x = value 
        elif key == 2:
            self._y = value
        else:
            raise IndexError(key)
            
    @Circle.radius.setter
    def radius(self, value):
        self._radius = float(value)

    @Circle.pos.setter
    def pos(self, value):
        self._x, self._y = value

if __name__ == '__main__':
    import doctest
    doctest.testmod()

    Circle(1, (1, 2))
    mCircle(2, (1, 2))