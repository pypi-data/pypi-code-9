# Author: Joel Frederico
"""
This project has slowly grown from frequently-used code snippets. The main objective is to create a collection of interconnected methods frequently needed to visualize and analyze data using `NumPy <http://www.numpy.org/>`_, `SciPy <http://www.scipy.org/>`_, `Matplotlib <http://matplotlib.org/>`_, and `PyQt4 <http://www.riverbankcomputing.com/software/pyqt/download>`_.
"""
__version__ = '1.4.5'
from . import accelphys
from . import facettools
from . import logging
from . import matplotlib
from . import numpy
from . import scipy
from . import utils

# class Error(Exception):
#     """Base class for exceptions in this module."""
#     pass
#
#
# class ArgumentError(Error):
#     """Exception raised for errors in function arguments.
#
#     Attributes:
#         arg -- input argument in which the error occurred
#         msg -- explanation of the error
#     """
#
#     def __init__(self, arg, msg):
#         self.arg = arg
#         self.msg = msg
