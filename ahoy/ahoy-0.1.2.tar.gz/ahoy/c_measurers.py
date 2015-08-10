from __future__ import print_function, division
from abc import ABCMeta, abstractmethod
import numpy as np
from ciabatta.meta import make_repr_str
from ahoy import measurers


class CMeasurer(measurers.Measurer):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_cs(self):
        return


class FieldCMeasurer(CMeasurer):

    def __init__(self, c_field, positions):
        self.c_field = c_field
        self.positions = positions

    def get_cs(self):
        return self.c_field.get_val_i(self.positions)

    def __repr__(self):
        fs = [('c_field', self.c_field)]
        return make_repr_str(self, fs)


class LinearCMeasurer(CMeasurer):

    def __init__(self, positions):
        self.positions = positions

    def get_cs(self):
        return self.positions.dr[:, 0]

    def __repr__(self):
        fs = []
        return make_repr_str(self, fs)


class GradCMeasurer(measurers.Measurer):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_grad_cs(self):
        return


class FieldGradCMeasurer(GradCMeasurer):

    def __init__(self, c_field, positions):
        self.c_field = c_field
        self.positions = positions

    def get_grad_cs(self):
        return self.c_field.get_grad_i(self.positions)

    def __repr__(self):
        fs = [('c_field', self.c_field)]
        return make_repr_str(self, fs)


class ConstantGradCMeasurer(GradCMeasurer):

    def __init__(self, n, dim):
        self.grad_c = np.zeros([n, dim])
        self.grad_c[:, 0] = 1.0

    @property
    def n(self):
        return self.grad_c.shape[0]

    @property
    def dim(self):
        return self.grad_c.shape[1]

    def get_grad_cs(self):
        return self.grad_c

    def __repr__(self):
        fs = []
        return make_repr_str(self, fs)
