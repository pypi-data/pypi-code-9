###############################################################################
#
#   Onyx Portfolio & Risk Management Framework
#
#   Copyright 2014 Carlo Sbraccia
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
###############################################################################

from onyx.datatypes.gcurve import GCurve

import numpy as np
import bisect

__all__ = ["Curve"]


# -----------------------------------------------------------------------------
def is_numlike(obj):
    """
    Helper function used to determine if an object behaves like a number.
    """
    try:
        obj + 1.0
    except:
        return False
    else:
        return True


###############################################################################
class Curve(GCurve):
    """
    Curve class based on GCurve and supporting numerical values only.
    """
    # -------------------------------------------------------------------------
    def __init__(self, dates=None, values=None, dtype=np.float64):
        """
        Description:
            Create a curve from a list of dates and a list of generic values.
            Raise a CurveError exception if dates and values don't have same
            length or if dates contains any duplicates.
        Inputs:
            dates  - list/array of Dates
            values - list/array of values
            dtype  - data type for the values (default is np.float64)
        """
        super().__init__(dates, values, dtype)

    # -------------------------------------------------------------------------
    #  A few methods for simple curve algebra. It's always assumed that the
    #  two curves are already aligned
    def __add__(self, other):
        crv = self.__new__(self.__class__)
        if isinstance(other, self.__class__):
            return crv.__init_raw__(self.dates,
                                    self.values + other.values, np.float64)
        else:
            return crv.__init_raw__(self.dates,
                                    self.values + other, np.float64)

    def __sub__(self, other):
        crv = self.__new__(self.__class__)
        if isinstance(other, self.__class__):
            return crv.__init_raw__(self.dates,
                                    self.values - other.values, np.float64)
        else:
            return crv.__init_raw__(self.dates,
                                    self.values - other, np.float64)

    def __mul__(self, other):
        crv = self.__new__(self.__class__)
        if isinstance(other, self.__class__):
            return crv.__init_raw__(self.dates,
                                    self.values * other.values, np.float64)
        elif is_numlike(other):
            return crv.__init_raw__(self.dates,
                                    self.values * other, np.float64)
        else:
            TypeError("cannot multiply a {0:s} "
                      "by a {1:s}".format(self.__class__, other.__class__))

    def __truediv__(self, other):
        crv = self.__new__(self.__class__)
        if isinstance(other, self.__class__):
            return crv.__init_raw__(self.dates,
                                    self.values / other.values, np.float64)
        elif is_numlike(other):
            return crv.__init_raw__(self.dates,
                                    self.values / other, np.float64)
        else:
            TypeError("cannot multiply a {0:s} "
                      "by a {1:s}".format(self.__class__, other.__class__))

    def __radd__(self, scalar):
        crv = self.__new__(self.__class__)
        return crv.__init_raw__(self.dates, scalar + self.values, np.float64)

    def __rsub__(self, scalar):
        crv = self.__new__(self.__class__)
        return crv.__init_raw__(self.dates, scalar - self.values, np.float64)

    def __rmul__(self, scalar):
        crv = self.__new__(self.__class__)
        return crv.__init_raw__(self.dates, scalar * self.values, np.float64)

    def __rtruediv__(self, scalar):
        crv = self.__new__(self.__class__)
        return crv.__init_raw__(self.dates, scalar / self.values, np.float64)
