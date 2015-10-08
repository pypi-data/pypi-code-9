#!/usr/bin/env python
from ctypes.util import find_library

from .._gcrypt import ffi
from .. import errors
from .mpi import MPIint

lib = ffi.dlopen(find_library("gcrypt"))

"""
This modules is used to define Elleptic Curve points
"""

class Point(object):
    """
    An elliptic curve point is basically a tuple of MPI
    """
    def __init__(self, ctx):
        """
        Initialize a Point using the MPI provided for x, y and z.
        Ctx is an elliptic curve context
        """
        self.__point = lib.gcry_mpi_point_new(0)
        self.__ctx = ctx

    def __del__(self):
        lib.gcry_mpi_point_release(self.__point)

    def set(self, point):
        """
        Set the coordinate of the point to the MPI provided
        for x, y and z.
        """
        lib.gcry_mpi_point_release(self.__point)
        self.__point = point

    def get(self):
        """
        Get the coordinate of the point and stores them in a 3-Tuple
        of MPI
        """
        return self.__point

    def __repr__(self):
        """
        Print the EC Point
        """
        return "({},{},{})".format(self['x'].value(), self['y'].value(), self['z'].value())

    def __getitem__(self, key):
        """
        Let's get the item specified by key
        """
        ret_mpi = MPIint()
        pointer = ret_mpi.get()

        if key == 'x':
            lib.gcry_mpi_point_get(pointer, ffi.NULL, ffi.NULL, self.get())
        elif key == 'y':
            lib.gcry_mpi_point_get(ffi.NULL, pointer, ffi.NULL, self.get())
        elif key == 'z':
            lib.gcry_mpi_point_get(ffi.NULL, ffi.NULL, pointer, self.get())
        else:
            raise KeyError

        if pointer == ffi.NULL:
            return None
        ret_mpi.set(pointer)
        return ret_mpi

    def __setitem__(self, key, value):
        """
        Let's set the coordinate of the point with MPI.
        """
        if not isinstance(value, MPIint):
            raise TypeError("We need an MPIint to be set as {}. {} given.".format(key, type(value)))

        (x, y, z) = (self['x'], self['y'], self['z'])
        if key == 'x':
            lib.gcry_mpi_point_set(self.get(), value.get(), y.get(), z.get())
        elif key == 'y':
            lib.gcry_mpi_point_set(self.get(), x.get(), value.get(), z.get())
        elif key == 'z':
            lib.gcry_mpi_point_set(self.get(), x.get(), y.get(), value.get())

    def affine(self, x, y):
        """
        Compute the affine coordinates from the projective coordinates in point
        and store them into x and y. If one coordinate is not required, NULL may
        be passed to x or y. ctx is the context object which has been created
        using gcry_mpi_ec_new. Returns 0 on success or not 0 if point is at
        infinity. 
        """
        if not isinstance(x, MPIint) or not isinstance(y, MPIint):
            raise TypeError("MPIint must be given for x and y to store the affine coordinate")

        ret = lib.gcry_mpi_ec_get_affine(x.get(), y.get(), self.get(), self.__ctx)
        return (x, y)

    def double(self):
        """
        Double the point u of the elliptic curve described by ctx and store the
        result into w.
        """
        point_dest = lib.gcry_mpi_point_new(0)
        lib.gcry_mpi_ec_dup(point_dest, self.get(), self.__ctx)
        self.set(point_dest)

    def __add__(self, point):
        """
        Add the points u and v of the elliptic curve described by ctx and store the result into w.
        """
        if not isinstance(point, Point):
            raise TypeError("Can only add Point to Point. Got {} instead.".format(type(point)))

        point_dest = lib.gcry_mpi_point_new(0)
        lib.gcry_mpi_ec_add(point_dest, self.get(), point.get(), self.__ctx)
        ret_point = Point(self.__ctx)
        ret_point.set(point_dest)
        return ret_point

    def __mul__(self, mpi):
        """
        Multiply the point u of the elliptic curve described by ctx by n and store the result into w.
        """
        if not isinstance(mpi, MPIint):
            raise TypeError("Can only multuply a point by a MPIint, got {} instead.".format(type(point)))

        point_dest = lib.gcry_mpi_point_new(0)
        lib.gcry_mpi_ec_mul(point_dest, mpi.get(), self.get(), self.__ctx)
        ret_point = Point(self.__ctx)
        ret_point.set(point_dest)
        return ret_point

    def __eq__(self, point):
        """
        Points are equal if they have the same coordinates
        """
        if not isinstance(point, Point):
            raise TypeError("Can only compare Point to Point, got {} instead.".format(type(point)))
        return (self['x'], self['y'], self['z']) == (point['x'], point['y'], point['z'])

    def isoncurve(self):
        """
        Return true if point is on the elliptic curve described by ctx. 
        """
        ret = lib.gcry_mpi_ec_curve_point(self.get(), self.__ctx)
        if ret >= 1:
            return True
        return False
