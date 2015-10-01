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

import numpy as np
import collections
import bisect

__all__ = ["GCurve", "Knot", "CurveError"]


###############################################################################
class CurveError(Exception):
    """
    Base class for all Curve exceptions.
    """
    pass


###############################################################################
class Knot(object):
    """
    Class representing a generic curve knot as a pair (date, value).
    """
    __slots__ = ("date", "value")

    # -------------------------------------------------------------------------
    def __init__(self, d, v):
        self.date = d
        self.value = v

    # -------------------------------------------------------------------------
    def __repr__(self):
        cls = self.__class__
        return "{.__name__:s}({.date!r},{.value!r})".format(cls, self, self)

    # -------------------------------------------------------------------------
    def __str__(self):
        if hasattr(self.value, "__str__"):
            return "{0!s}, {1!s}".format(self.date, self.value)
        else:
            return "{0!s}, unprintable value...".format(self.date)

    # -------------------------------------------------------------------------
    #  methods for knot comparison (date based)
    def __lt__(self, other):
        return self.date < other.date

    def __le__(self, other):
        return self.date <= other.date

    def __gt__(self, other):
        return self.date > other.date

    def __ge__(self, other):
        return self.date >= other.date

    # -------------------------------------------------------------------------
    #  quality/inquality are based on both date and value
    def __eq__(self, other):
        return self.date == other.date and self.value == other.value

    def __ne__(self, other):
        return self.date != other.date or self.value != other.value


###############################################################################
class GCurve(object):
    """
    Base curve class implementing the core functionality. The internal
    representation is optimized for fast lookup (ln(N)) and quick access to
    dates and values. Inserts and deletes are slow.
    """
    # -------------------------------------------------------------------------
    def __init__(self, dates=None, values=None, dtype=np.object):
        """
        Description:
            Create a curve from a list of dates and a list of generic values.
            Raise a CurveError exception if dates and values don't have same
            length or if dates contains any duplicates.
        Inputs:
            dates  - list/array of Dates
            values - list/array of values
            dtype  - data type for the values (default is np.object)
        """
        if dates is None: dates = []    # analysis:ignore
        if values is None: values = []  # analysis:ignore

        if len(dates) != len(values):
            raise CurveError("Input dates and values are of different length")

        # --- check whether there are any duplicates in dates
        if len(dates) != len(set(dates)):
            duplicates = {x: y for x, y
                          in collections.Counter(dates).items() if y > 1}
            raise CurveError("Creating curve with duplicate "
                             "dates: {0:s}".format(duplicates.__repr__()))

        # --- sort by date and call raw constructor
        data = sorted(zip(dates, values), key=lambda knot: knot[0])
        self.__init_raw__([d for (d, v) in data],
                          [v for (d, v) in data], dtype)

    # -------------------------------------------------------------------------
    def __init_raw__(self, dates, values, dtype):
        self.dtype = dtype
        self.dates = np.array(dates, dtype=np.object)
        self.values = np.array(values, dtype=dtype)
        return self

    # -------------------------------------------------------------------------
    def __deepcopy__(self, memo):
        clone = self.__class__.__new__(self.__class__)
        memo[id(self)] = clone
        clone.dates = self.dates.copy()
        clone.values = self.values.copy()
        clone.dtype = self.dtype
        return clone

    # -------------------------------------------------------------------------
    #  methods for curve comparison
    def __eq__(self, other):
        return np.all(self.dates == other.dates) and \
               np.all(self.values == other.values)

    def __ne__(self, other):
        return np.any(self.dates != other.dates) and \
               np.any(self.values != other.values)

    # -------------------------------------------------------------------------
    #  support serialization
    def __getstate__(self):
        return self.dates, self.values, self.dtype

    def __setstate__(self, state):
        self.dates, self.values, self.dtype = state

    # -------------------------------------------------------------------------
    def __repr__(self):
        cls = self.__class__.__name__
        dts = self.dates.tolist()
        vls = self.values.tolist()
        return "{0:s}(dates={1!r}, values={2!r})".format(cls, dts, vls)

    # -------------------------------------------------------------------------
    def __str__(self):
        return "\n".join([Knot(d, v).__str__()
                          for d, v in zip(self.dates, self.values)])

    # -------------------------------------------------------------------------
    #  GCurve is an iterable container type: implement some relevant methods
    def __len__(self):
        return len(self.dates)

    def __iter__(self):
        return zip(self.dates, self.values)

    def __getitem__(self, date):
        idx = self.dates.searchsorted(date)
        if self.dates[idx] == date:
            return self.values[idx]
        else:
            raise IndexError

    def __setitem__(self, date, val):
        idx = self.dates.searchsorted(date)
        if idx == len(self.dates):
            self.dates = np.append(self.dates, date)
            self.values = np.append(self.values, val)
        elif self.dates[idx] == date:
            self.values[idx] = val
        else:
            self.dates = np.insert(self.dates, idx, date)
            self.values = np.insert(self.values, idx, val)

    def __delitem__(self, date):
        idx = self.dates.searchsorted(date)
        if self.dates[idx] == date:
            self.dates = np.delete(self.dates, idx)
            self.values = np.delete(self.values, idx)
        else:
            raise IndexError

    def __contains__(self, date):
        dts = self.dates
        if not len(dts):
            return False
        if date < dts[0] or date > dts[-1]:
            return False
        if dts[dts.searchsorted(date)] == date:
            return True
        else:
            return False

    # -------------------------------------------------------------------------
    @property
    def ordinals(self):
        """
        Return an array of dates in numeric format.
        """
        return np.fromiter((d.ordinal for d in self.dates),
                           dtype=float, count=len(self.dates))

    # -------------------------------------------------------------------------
    @property
    def front(self):
        """
        Description:
            Return the first knot of the curve.
        Returns:
            A knot.
        """
        return Knot(self.dates[0], self.values[0])

    @property
    def back(self):
        """
        Description:
            Return the last knot of the curve.
        Returns:
            A knot.
        """
        return Knot(self.dates[-1], self.values[-1])

    # -------------------------------------------------------------------------
    def crop(self, start=None, end=None):
        """
        Description:
            Return a sub-curve with knots that fall within the specified range.
            If start date or end date are not set, use the current extremes of
            the curve.
        Inputs:
            start - the start of the range (included)
            end   - the   end of the range (included)
        Return:
            A sub-curve of the original curve.
        """
        if not len(self.dates):
            return self

        # --- store dates in local variable for faster access
        dts = self.dates

        if start is None:
            i = 0
        else:
            i = bisect.bisect_left(dts, start)

        if end is None:
            j = -1
        else:
            j = bisect.bisect_right(dts, end, i)

        crv = self.__new__(self.__class__)
        return crv.__init_raw__(dts[i:j], self.values[i:j], self.dtype)
