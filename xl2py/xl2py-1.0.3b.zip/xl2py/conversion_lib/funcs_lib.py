# -*- coding: utf-8 -*-
from __future__ import division, absolute_import, print_function

from . import *
from .. import __author__, __version__
from ..core import np as np

class Funlib(object):
    """ Funlib
    This class must be loaded by xl2py.core.processor as Funlib to parse
    its simple lambda conversion references or customized conversion functions (e.g. pyxl_error)
    """

    def __init__(self):
        # xl to py formulas conversion for eval()
        self.conversion_reference = dict()
        self.__author__ = __author__
        self.__version__ = __version__

        # xl to py formula conversion
        xlformulas = ['IF', 'AVERAGE', 'STDEV.P', '^', 'TRANSPOSE', 'ABS', 'MMULT', 'IFERROR', 'SUM', 'COUNT','SQRT']
        params = [[3, 3],[1,1],[1,1],[0,0],[1,1],[1,1],[2,2],[2,2],[1,1],[1,1],[1,1]] # 2 arguments from first argument in xl, separated by '/'
        pyxlformulas = [lambda args : ''.join(['('+str(args[0])+').astype(float)*('+str(args[1])+')+(-('+str(args[0])+')).astype(float)*('+str(args[2])+')']),\
                    lambda args : ''.join(['np.average(',str(args[0]),')']),\
                    lambda args : ''.join(['np.std(',str(args[0]),')']),\
                    '**',\
                    lambda args : ''.join(['np.transpose(',str(args[0]),')']),\
                    lambda args : ''.join(['np.abs(',str(args[0]),')']),\
                    lambda args : ''.join(['np.dot(',str(args[0]),',',str(args[1]),')']),\
                    lambda args : ''.join(['self.Funlib.pyxl_error(',str(args[0]),',',str(args[1]),')']),\
                    lambda args : ''.join(['np.sum(',str(args[0]),')']),\
                    lambda args : ''.join(['np.size(',str(args[0]),')']),\
                    lambda args : ''.join(['np.sqrt(',str(args[0]),')'])]
        self.pycond  = {'<':'<','>':'>','<=':'<=','>=':'>=','<>':'!=','=':'=='}
        for i in range(0, len(xlformulas)):
            self.__gen_conversion_library(xlformulas[i],params[i],pyxlformulas[i])

    def __gen_conversion_library(self,xlFormula,xlParams,pyFormula):
        """ internal method gen_conversion_library
        generate a conversion dictionary _conversion_referene which ties a
        lambda or nested-type Python formula to a XL-type formula
        """
        # generate msexcel formula to python referenced formula conversion
        self.conversion_reference.__setitem__(xlFormula,dict())
        self.conversion_reference[xlFormula].__setitem__('xlParams',xlParams)
        self.conversion_reference[xlFormula].__setitem__('pyFormula',pyFormula)

    def pyxl_error(self,x,y):
        """ pyxl_error (substitute for XL fun IFERR)
        params (2):
            x as numeric or numeric array
            y as numeric
        returns x with nan and inf values converted to y
        """
        if type(x) is not np.ndarray:
            x = np.array(x)
        if any(np.isnan(x)+np.isinf(x)):
            x[np.isnan(x)+np.isinf(x)] = y
        return x.tolist()