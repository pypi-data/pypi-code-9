###############################################################################
#
#   Agora Portfolio & Risk Management System
#
#   Copyright 2015 Carlo Sbraccia
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

from onyx.core import RDate, HolidayCalendar, GetObj
from onyx.datatypes.date_functions import DateRange as __date_range

__all__ = ["DateOffset", "DateRange"]


# -----------------------------------------------------------------------------
def DateOffset(date, rule, calendar=None):
    """
    Description:
        Applies the specified rule (a string, as defined below) to the
        specified date to obtain a new shifted date.
    Inputs:
        date     - date on which the date-rule is to be applied
        rule     - a tag specifying shift relative to input date
        calendar - a holiday calendar name used to identify business days
    Rule definitions:
        d = add calendar day
        b = add business day
        w = add calendar week
        m = add calendar month
        y = add calendar year
        c = go to the required day in the month
        e = go to end of month (ignores num)
        J = go to first calendar day of month (ignores num)
        M = go to closest Monday as specified by num
        F = go to closest Friday as specified by num
        q = go to beginning of the quarter (ignores num)
        Q = go to end of the quarter (ignores num)
        A = go to beginning of the year (ignores num)
        E = go to end of the year (ignores num)
    Returns:
        A Date.
    Examples:
        EndOfMonth = DateOffset(Date.today(), "+e")
        FirstBizDayOf2000 = DateOffset(Date(2000, 1, 1), "+b")
    """
    if calendar is None or isinstance(calendar, HolidayCalendar):
        pass
    elif isinstance(calendar, str):
        calendar = GetObj(calendar)
    else:
        raise ValueError("calendar must be either a string or "
                         "an instance of HolidayCalendar (a {0:s} "
                         "was passed instead).".format(type(calendar)))

    return date + RDate(rule, calendar)


# -----------------------------------------------------------------------------
def DateRange(start, end, rule, calendar=None):
    """
    Description:
        Iterator that yields a series of dates between start date and
        end date according to increment rule (start date is included).
    Inputs:
        start    - the first date in the range
        end      - the last  date in the range
        rule     - a date rule (see RDate)
        calendar - a holiday calendar used to identify business days
    Yields:
        A range of Dates.
    """
    if calendar is None or isinstance(calendar, HolidayCalendar):
        pass
    elif isinstance(calendar, str):
        calendar = GetObj(calendar)
    else:
        raise ValueError("calendar must be either a string or "
                         "an instance of HolidayCalendar (a {0:s} "
                         "was passed instead).".format(type(calendar)))

    for d in __date_range(start, end, rule, calendar):
        yield d
