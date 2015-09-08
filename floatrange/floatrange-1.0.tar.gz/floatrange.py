 #!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""floatrange - range() like with float numbers.

:author: Laurent Pointal <laurent.pointal@laposte.net>
:copyright: Laurent Pointal, 2011-2015
:license: MIT
:version: 0.2b


Usage example
-------------

(note computation approximation and display with floats)

>>> from floatrange import floatrange
>>> floatrange(5)
floatrange(0.0, 5.0, 1.0)
>>> list(floatrange(5))
[0.0, 1.0, 2.0, 3.0, 4.0]
>>> list(floatrange(3.2,5.4,0.2))
[3.2, 3.4000000000000004, 3.6, 3.8000000000000003, 4.0, 4.2, 4.4,
4.6000000000000005, 4.800000000000001, 5.0, 5.2]
>>> 6 in floatrange(1,8)
True
>>> 6.1 in floatrange(1,8,1,prec=0.2)
True
>>> 6.1 in floatrange(1,8,1,prec=0.05)
False
>>> list(reversed(floatrange(5)))
[4.0, 3.0, 2.0, 1.0, 0.0]
>>> list(floatrange(10.1,9.7,-0.1))
[10.1, 10.0, 9.9, 9.799999999999999]


"""
# Copyright (C) 2011 by Laurent Pointal <laurent.pointal@laposte.net>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# Same behavior with Python2 than Python3 on:
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

__version__ = '1.0'


# Note: floatrange class name choosen to match with range.
class floatrange(object):
    """floatrange([start,] stop[, step[, prec]]) -> floatrange object

    Build a virtual sequence of floating point numbers from ``start`` to
    ``stop`` by ``step``.
    Set float equality precision with ``prec`` (default 0 for strict equality).

    Unlike Python range(), generated values are floating point.
    Like Python range(), the ``stop`` value is *not* included
    (to have the stop value included, just add step*0.1 to it).

    A :class:`floatrange` object is usable like Python :class:`range`,
    to iterate on the values, to test for its length, to get the
    value at an index, to get length of values sequence, to search for the
    index of a value, to count the number of occurrences of a value.

    As floating point computation may lead to slightly different values,
    you should take care:

    - Test for presence of a value in the range use ``prec``, which is
      by default zero for *exact* equality.
    - When reverting the :class:`floatrange`, the new object is created to
      *generate* reverse values, this can build values with computational
      differences.
      To have exact same values in reverse order, cast to a :class:`list`
      and reverse it.

    """
    #  _start/_stop/_step/_prec attributes should never be modified.
    def __init__(self, start, stop=None, step=None, prec=0):
        """Initialization of a floatrange objet.

        :param start: beginning of the range, default to 0.
        :type start: float
        :param stop: end of the range, not included.
        :type stop: float
        :param step: step between two consecutive values of the range,
        :            default to 1.
        :type step: float
        :param prec: maximum difference for float values equality,
        :            default to 0.0.
        :type prec: float
        """
        if step is None:
            step = 1
        if stop is None:
            stop = start
            start = 0
        if step == 0:
            raise ValueError("FloatRange() arg 'step' must not be zero")
        # Store values, ensure they are floats (may raise ValueError
        # exception).
        self._start = float(start)
        self._stop = float(stop)
        self._step = float(step)
        self._prec = abs(float(prec))
        # Pre-caculate length once.
        self._calculate_length()
        # for no-empty sequences, must have step>2*prec.
        if self._length > 0 and self._prec > 0:
            if self._step <= 2 * self._prec:
                raise ValueError("FloatRange() step must be greater "
                                 "than 2*prec'")

    def _calculate_length(self):
        """Compute and store float range length."""
        if self._step == 0 or (self._stop - self._start) / self._step <= 0 or \
                           self._floatcomp(self._start, self._stop) == 0:
            self._length = 0
        else:
            # Calculate number of steps to reach stop from start with step.
            n = (self._stop - self._start) / self._step
            nint = int(n)
            # Special case if it is not an integer count.
            self._length = nint if n == nint else nint + 1

    def __len__(self):
        """Return count of range values.

        :return: count or float range values.
        :rtype: int
        """
        return self._length

    def __contains__(self, item):
        """x.__contains__(y) <==> y in x

        .. warning::

            If precision is zero (default), floating point comparison
            may fail due to small computational difference.

        :param item: value to test for presence in the float range.
        :type item: float
        :return: presence test result
        :rtype: bool
        """
        if self._length == 0:
            return False
        if not isinstance(item, (float, int)):
            return False
        item = float(item)
        # First, check if item is between both edges of the range.
        if self._start < self._stop:
            if self._floatcomp(self._start, item) > 0 or \
                                    self._floatcomp(self._stop, item) <= 0:
                return False
        else:
            if self._floatcomp(self._stop, item) >= 0 or \
                                    self._floatcomp(self._start, item) < 0:
                return False

        index = (item - self._start) / self._step
        if index == int(index):
            # The item is an exact value of the sequence if it is at an
            # integer step index when considering sequence values.
            return True
        else:
            # The item is considered to be like a sequence value if it is
            # near that value with precision distance.
            index = round(index)
            return (self._floatcomp(item, self[int(index)]) == 0)

    def __repr__(self):
        """x.__repr__() <==> repr(x)"""
        if self._prec == 0:
            return "floatrange({}, {}, {})".format(self._start, self._stop,
                                                    self._step)
        else:
            return "floatrange({}, {}, {}, prec={})".format(self._start,
                                        self._stop, self._step, self._prec)

    def __str__(self):
        """x.__str__() <==> str(x)"""
        # For user printable string, we use same representation.
        return self.__repr__()

    def __getitem__(self, key):
        """x.__getitem__(y) <==> x[y]

        :param key: index of float range item to get.
        :type key: int
        :return: value of item at the index key
        :rtype: float
        """
        key = self._index_adjust_check(key)
        return self._start + key * self._step

    def _index_adjust_check(self, index):
        """Check index type and map negative index to positive counterpart.

        :param index: index to adjust
        :type index: int
        :return: index mapped in positive values (or raised exception).
        :rtype: int
        """
        if type(index) != type(0):
            raise TypeError("floatrange indices must be integers")

        if -self._length <= index < 0:
            return self._length + index
        elif 0 <= index < self._length:
            return index
        else:
            raise IndexError("floatrange index out of range")

    def __reversed__(self):
        """Returns a reverse float range iterator.

        Warning: Floating point reversed range may slightly vary in values due
        to small computational differences. To have exactly same values in
        reversed order, cast to a list and reverse the list.

        :return: floatrange producing inverse sequence of floats
        :rtype: floatrange
        """
        if self._length == 0:
            return self
        # To ensure we have same values (but reversed) in the range:
        #       For reversed's start, we use last range value (not stop).
        #       For reversed's stop, we go one tenth of step before the start
        #       to ensure its inclusion.
        return floatrange(self[-1], self._start - self._step * 0.1,
                            -self._step)

    def _floatcomp(self, x, y):
        """Compare v1 to v2 using the precision attribute of the FloatRange.

        :return: comparison result, <0 or 0 or >0
            * zero if x == y at +-precision,
            * negative if x < y,
            * strictly positive if x > y.
        :rtype: int
        """
        if abs(x - y) <= self._prec:
            return 0
        elif x < y:
            return -1
        else:
            return 1

    def count(self, value):
        """x.count(value) -> integer -- nb occurrences of value in x

        As these are step consecutive values,  count is 1 if value is in
        sequence, else it is 0.
        The 'in' meaning must be interpreted with precision in mind.

        :param value: value to count the number of occurrences.
        :type value: float
        :return: count of occurrences of value in the floatrange (0 or 1).
        :rtype: int
        """
        if value in self:
            return 1
        else:
            return 0

    def index(self, value, start=None, stop=None):
        """x.index(value,[start,[stop]])->integer -- index of value in x

        If the value is not in float range, a ValueError exception is raised.
        The 'in' meaning must be interpreted with precision in mind.

        :param value: value to search for first occurrence.
        :type value: float
        :param start: begin index to restrain value search within the
                      floatrange.
        :type start: int
        :param stop: end index to restrain value search within the floatrange.
        :type stop: int
        :return: index of the value in the floatrange.
        :rtype: int
        """
        if value not in self:
            raise ValueError("{} not in floatrange".format(value))
        idx = int(round((value - self._start) / self._step))
        if start is not None and idx < self._index_adjust_check(start):
            raise ValueError("{} not in floatrange".format(value))
        if stop is not None and idx >= self._index_adjust_check(stop):
            raise ValueError("{} not in floatrange".format(value))

        return idx

    class _FloatRangeIterator(object):
        """Iterator on a range of floating point values.
        """
        def __init__(self, fr):
            self.fr = fr
            self.curindex = 0

        def __iter__(self):
            return self

        def __next__(self):
            fr = self.fr
            cur = fr._start + fr._step * self.curindex
            # Check if we reach the end.
            if fr._step > 0:
                if cur >= fr._stop:
                    raise StopIteration
            else:
                if cur <= fr._stop:
                    raise StopIteration
            # Prepare next iteration and return current one.
            self.curindex += 1
            return cur

        def next(self):
            # For Python 2 compatibility.
            return self.__next__()

    def __iter__(self):
        """x.__iter__() <==> iter(x)"""
        return floatrange._FloatRangeIterator(self)


if __name__ == '__main__':
    import unittest

    class FloatRangeTest(unittest.TestCase):

        def test_construction(self):
            r = floatrange(3)
            self.assertListEqual(list(r), [0.0, 1.0, 2.0],
                                    msg="construction with stop")
            r = floatrange(1, 4)
            self.assertListEqual(list(r), [1.0, 2.0, 3.0],
                                    msg="construction with start,stop")
            r = floatrange(0.5, 2.0, 0.5)
            self.assertListEqual(list(r), [0.5, 1.0, 1.5],
                                    msg="construction with start,stop,step")
            r = floatrange(2.0, 0.5, -0.5)
            self.assertListEqual(list(r), [2.0, 1.5, 1.0],
                            msg="construction with start,stop,negative step")

        def test_construction_null_step_exception(self):
            self.assertRaises(ValueError, floatrange, 10, 12, 0)

        def test_construction_step_lt_prec_exception(self):
            self.assertRaises(ValueError, floatrange, 10, 12, 0.2, 0.5)

        def test_length(self):
            r = floatrange(1, 11, 2)
            self.assertEqual(len(r), len(list(r)))
            r = floatrange(0, 0)
            self.assertEqual(len(r), len(list(r)), "empty range")
            r = floatrange(0, 10, 0.5)
            self.assertEqual(len(r), len(list(r)))
            r = floatrange(10, 5, -0.5)
            self.assertEqual(len(r), len(list(r)))
            r = floatrange(10)
            self.assertEqual(len(r), len(list(r)))
            r = floatrange(3, 10)
            self.assertEqual(len(r), len(list(r)))
            r = floatrange(1, 10, 2)
            self.assertEqual(len(r), len(list(r)))
            r = floatrange(10, 1, -1)
            self.assertEqual(len(r), len(list(r)))
            r = floatrange(1, 10, -0.5)
            self.assertEqual(len(r), len(list(r)), "empty range")

        def test_contains(self):
            self.assertEqual(0.0 in floatrange(0, 10, 0.5), True,
                            msg="contains, first value")
            self.assertEqual(5.0 in floatrange(0, 10, 0.5), True,
                            msg="contains, middle value")
            self.assertEqual(5.1 in floatrange(0, 10, 0.5), False,
                            msg="not contains, outside exact precision")
            self.assertEqual(5.1 in floatrange(0, 10, 0.5, prec=0.2), True,
                            msg="contains, inside precision")
            self.assertEqual(-0.1 in floatrange(0, 10, 0.5, prec=0.2), True,
                            msg="contains, before first but inside precision")
            self.assertEqual(0.3 in floatrange(0, 10, 0.5, prec=0.1), False,
                            msg="not contains, outside precision")
            self.assertEqual(10.0 in floatrange(0, 10, 0.5), False,
                            msg="not contains, stop value")
            self.assertEqual(9.9 in floatrange(0, 10, 0.5, prec=0.2), False,
                            msg="not contains, inside precision of stop value")
            self.assertEqual(9.6 in floatrange(0, 10, 0.5, prec=0.2), True,
                            msg="contains, last value inside precision")
            self.assertEqual(10.0 in floatrange(100, 10, -10), False,
                            msg="not contains, stop value with negative step.")

        def test_count(self):
            self.assertEqual(floatrange(10).count(5), 1,
                            msg="middle value contained")
            self.assertEqual(floatrange(5, 10).count(3), 0,
                            msg="value out of floatrange")
            self.assertEqual(floatrange(10).count(0), 1,
                            msg="first value counted in floatrange")
            self.assertEqual(floatrange(10).count(10), 0,
                            msg="last value not counted")
            self.assertEqual(floatrange(1, 5, 0.1).count(1.0 + 9 * 0.1), 1,
                            msg="computed value to be exact")
            self.assertEqual(floatrange(1, 5, 0.1).count(3.300000001), 0,
                            msg="exact value dont match item")
            self.assertEqual(floatrange(1, 5, 0.1, 0.02).count(3.3), 1,
                            msg="value matched with precision")

        def test_index(self):
            self.assertEqual(floatrange(10).index(5), 5,
                            msg="index of middle value")
            self.assertRaises(ValueError, floatrange(5, 10).index, 3)
                            # Clearly out of range
            self.assertRaises(ValueError, floatrange(5, 10).index, 10)
                            # Last value is out of range
            self.assertEqual(floatrange(4, 12, 0.001).index(4), 0,
                            msg="index of first value")
            self.assertEqual(floatrange(1, 4, 0.5).index(1 + 5 * 0.5), 5,
                            msg="index of last value in range")
            self.assertEqual(floatrange(0, 10, 1, prec=0.1).index(1.01), 1,
                            msg="within range using precision")
            self.assertEqual(floatrange(0, 10, 1, prec=0.1).index(-0.01), 0,
                            msg="first value within range using precision")
            self.assertEqual(floatrange(0, 10, 1, prec=0.1).index(-0.01), 0,
                            msg="just before range using precision")
            self.assertEqual(floatrange(0, 10, 1, prec=0.1).index(9.1), 9,
                            msg="last value within range using precision")
            self.assertRaises(ValueError, floatrange(0, 10, 1, prec=0.1).index,
                        9.100000001)    # just after range using precision

        def test_reverse(self):
            r = floatrange(0, 3, 0.3)
            r2 = reversed(r)
            self.assertEqual(len(r), len(r2),
                            msg="reverse must has same length")
            for i in range(len(r)):
                self.assertAlmostEqual(r[i], r2[len(r) - i - 1],
                            msg="item {} badly reversed".format(i))

    unittest.main()
