# Copyright (C) 2015 Chintalagiri Shashank
#
# This library is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
IEC60063 API
------------
"""

from decimal import Decimal


#: The E192 Number Series
E192 = list(map(Decimal, ['1.00', '1.01', '1.02', '1.04', '1.05', '1.06', '1.07',
                          '1.09', '1.10', '1.11', '1.13', '1.14', '1.15', '1.17',
                          '1.18', '1.20', '1.21', '1.23', '1.24', '1.26', '1.27',
                          '1.29', '1.30', '1.32', '1.33', '1.35', '1.37', '1.38',
                          '1.40', '1.42', '1.43', '1.45', '1.47', '1.49', '1.50',
                          '1.52', '1.54', '1.56', '1.58', '1.60', '1.62', '1.64',
                          '1.65', '1.67', '1.69', '1.72', '1.74', '1.76', '1.78',
                          '1.80', '1.82', '1.84', '1.87', '1.89', '1.91', '1.93',
                          '1.96', '1.98', '2.00', '2.03', '2.05', '2.08', '2.10',
                          '2.13', '2.15', '2.18', '2.21', '2.23', '2.26', '2.29',
                          '2.32', '2.34', '2.37', '2.40', '2.43', '2.46', '2.49',
                          '2.52', '2.55', '2.58', '2.61', '2.64', '2.67', '2.71',
                          '2.74', '2.77', '2.80', '2.84', '2.87', '2.91', '2.94',
                          '2.97', '3.01', '3.05', '3.09', '3.12', '3.16', '3.20',
                          '3.24', '3.28', '3.32', '3.36', '3.40', '3.44', '3.48',
                          '3.52', '3.57', '3.61', '3.65', '3.70', '3.74', '3.79',
                          '3.83', '3.88', '3.92', '3.97', '4.02', '4.07', '4.12',
                          '4.17', '4.22', '4.27', '4.32', '4.37', '4.42', '4.48',
                          '4.53', '4.59', '4.64', '4.70', '4.75', '4.81', '4.87',
                          '4.93', '4.99', '5.05', '5.11', '5.17', '5.23', '5.30',
                          '5.36', '5.42', '5.49', '5.56', '5.62', '5.69', '5.76',
                          '5.83', '5.90', '5.97', '6.04', '6.12', '6.19', '6.26',
                          '6.34', '6.42', '6.49', '6.57', '6.65', '6.73', '6.81',
                          '6.90', '6.98', '7.06', '7.15', '7.23', '7.32', '7.41',
                          '7.50', '7.59', '7.68', '7.77', '7.87', '7.96', '8.06',
                          '8.16', '8.25', '8.35', '8.45', '8.56', '8.66', '8.76',
                          '8.87', '8.98', '9.09', '9.20', '9.31', '9.42', '9.53',
                          '9.65', '9.76', '9.88']))

#: The E96 Number Series
E96 = [elem for idx, elem in enumerate(E192) if idx % 2 == 0]

#: The E48 Number Series
E48 = [elem for idx, elem in enumerate(E96) if idx % 2 == 0]

#: The E24 Number Series
E24 = list(map(Decimal, ['1.0', '1.1', '1.2', '1.3', '1.5', '1.6', '1.8', '2.0',
                         '2.2', '2.4', '2.7', '3.0', '3.3', '3.6', '3.9', '4.3',
                         '4.7', '5.1', '5.6', '6.2', '6.8', '7.5', '8.2', '9.1']))

#: The E12 Number Series
E12 = [elem for idx, elem in enumerate(E24) if idx % 2 == 0]

#: The E6 Number Series
E6 = [elem for idx, elem in enumerate(E12) if idx % 2 == 0]

#: The E3 Number Series
E3 = [elem for idx, elem in enumerate(E6) if idx % 2 == 0]

#: Order Strings for Capacitors
cap_ostrs = ['fF', 'pF', 'nF', 'uF', 'mF', 'F']

#: Order Strings for Resistors
res_ostrs = ['m', 'E', 'K', 'M', 'G']

#: Order Strings for Zener Diodes
zen_ostrs = ['V']

#: Order Strings for Inductors
ind_ostrs = ['nH', 'uH', 'mH']

#: Order Strings for Numbers
num_ostrs = ['']


def get_ostr(stype=None):
    """
    Given a device type, returns the order strings to be used for
    that type.

    Supports the following types:
        - ``resistor``
        - ``capacitor``
        - ``zener``
        - ``inductor``
        - ``number`` (Default)

    :param stype: The type of component you want the order strings for.
    :return: list

    """
    if stype == 'resistor':
        return res_ostrs
    if stype == 'capacitor':
        return cap_ostrs
    if stype == 'zener':
        return zen_ostrs
    if stype == 'inductor':
        return ind_ostrs
    return num_ostrs


def get_series(seriesst):
    """
    Given a specific series name, returns the Number series.

    Supports the following series:
        - ``E192``
        - ``E96``
        - ``E48``
        - ``E24``
        - ``E12``
        - ``E6``
        - ``E3``

    :param seriesst: The IEC60063 series you want.
    :return: list

    """
    if seriesst == 'E192':
        return E192
    elif seriesst == 'E96':
        return E96
    elif seriesst == 'E48':
        return E48
    elif seriesst == 'E24':
        return E24
    elif seriesst == 'E12':
        return E12
    elif seriesst == 'E6':
        return E6
    elif seriesst == 'E3':
        return E3
    raise ValueError(seriesst)


def gen_vals(series, ostrs, start=None, end=None):
    """
    Generate values for a specific type over a specific series within an
    optional range.

    The ``series`` parameter would typically be a string, naming one of
    the standard IEC60063 series. It could also be an arbitrary list of
    numbers (:class:`decimal.Decimal` is recommended).

    Similarly, the ``ostrs`` parameter would be a string naming one of the
    component types supported. You can provide a list of order strings
    of your own choosing instead.

    For each order string in ostrs, if a list is provided, or the list of
    strings returned by :func:`get_ostr`, this will generate all values of the
    series between 1 and 999, both included, subject to start / end conditions
    that may be specified using those parameters.

    If the start and / or end is not specified, this function will return all
    the possible values, given the order strings it has available.

    :param series: Which IEC60063 series to use. See :func:`get_series`.
    :type series: str
    :param ostrs: What order strings to append to the numbers. See :func:`get_ostr`.
    :type ostrs: str
    :param start: The value to start from. This value must be a part of the series.
    :type start: str
    :param end: The value to end at. This value must be a part of the series.
    :type end: str
    :return: A generator which produces all the values within the range.
    :rtype: generator

    """
    if isinstance(series, str):
        series = get_series(series)
    if isinstance(ostrs, str):
        ostrs = get_ostr(ostrs)
    if start is None:
        in_range = True
    else:
        in_range = False
    vfmt = lambda d: str(d.quantize(Decimal(1)) if d == d.to_integral() else d.normalize())
    for ostr in ostrs:
        for decade in range(3):
            for value in series:
                valstr = vfmt(value * (10 ** decade)) + ostr
                if in_range is False:
                    if valstr == start:
                        in_range = True
                if in_range is True:
                    yield valstr
                    if valstr == end:
                        return
