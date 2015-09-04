# -*- coding: utf-8 -*-
from __future__ import absolute_import
import time
import pytz
from pandas import date_range
from pandas import Series
import numpy as np

def datetime_to_epoch(dt):
    from datetime import datetime

    if dt.tzinfo is None:
        raise Exception("Cannot perform conversion on a timezone-naive datetime")

    d = (dt - UTC(1970, 1, 1))
    return int(d.total_seconds())

def datetime_to_seconds(dt):
    from datetime import datetime

    if dt.tzinfo is None:
        raise Exception("Cannot perform conversion on a timezone-naive datetime")

    d = (dt - UTC(1970, 1, 1))
    return int(d.total_seconds())

def datetime_to_milliseconds(dt):
    from datetime import datetime

    if dt.tzinfo is None:
        raise Exception("Cannot perform conversion on a timezone-naive datetime")

    d = (dt - UTC(1970, 1, 1))
    return int(d.total_seconds() * 1e3)

def datetime_to_microseconds(dt):
    from datetime import datetime

    if dt.tzinfo is None:
        raise Exception("Cannot perform conversion on a timezone-naive datetime")

    d = (dt - UTC(1970, 1, 1))
    return int(d.total_seconds() * 1e6)

def timedelta_to_seconds(td):
    return int(td.total_seconds())

def timedelta_to_milliseconds(td):
    return int(td.total_seconds() * 1e3)

def timedelta_to_microseconds(td):
    return int(td.total_seconds() * 1e6)


def eastern_time(*args):
    from datetime import datetime
    eastern = pytz.timezone('US/Eastern') 
    if len(args) == 1 and isinstance(args[0], datetime):
        if not args[0].tzinfo:
            return eastern.localize(args[0])
        else:
            return args[0].astimezone(eastern)
    return eastern.localize(datetime(*args))

def pacific_time(*args):
    from datetime import datetime
    pacific = pytz.timezone('US/Pacific') 
    if len(args) == 1 and isinstance(args[0], datetime):
        if not args[0].tzinfo:
            return pacific.localize(args[0])
        else:
            return args[0].astimezone(pacific)
    return pacific.localize(datetime(*args))

def central_time(*args):
    from datetime import datetime
    central = pytz.timezone('US/Central') 
    if len(args) == 1 and isinstance(args[0], datetime):
        if not args[0].tzinfo:
            return central.localize(args[0])
        else:
            return args[0].astimezone(central)
    return central.localize(datetime(*args))

def mountain_time(*args):
   from datetime import datetime
   mountain = pytz.timezone('US/Mountain') 
   if len(args) == 1 and isinstance(args[0], datetime):
      if not args[0].tzinfo:
         return mountain.localize(args[0])
      else:
         return args[0].astimezone(mountain)
   return mountain.localize(datetime(*args))

def taipei_time(*args):
    from datetime import datetime
    taipei = pytz.timezone('Asia/Taipei') 
    if len(args) == 1 and isinstance(args[0], datetime):
        if not args[0].tzinfo:
            return taipei.localize(args[0])
        else:
            return args[0].astimezone(taipei)
    return taipei.localize(datetime(*args))

def UTC(*args):
    from datetime import datetime 
    if len(args) == 1 and isinstance(args[0], datetime):
        if not args[0].tzinfo:
            return pytz.utc.localize(args[0])
        else:
            return args[0].astimezone(pytz.utc)
    return pytz.utc.localize(datetime(*args))

def eastern_datetime_to_UTC(datetime):
    edt = datetime
    if not datetime.tzinfo:
        eastern = pytz.timezone('US/Eastern') 
        edt = eastern.localize(datetime)
    return edt.astimezone(pytz.utc)

def taipei_datetime_to_UTC(datetime):
    nst = datetime
    if not datetime.tzinfo:
        taipei = pytz.timezone('Asia/Taipei')
        nst = taipei.localize(datetime)
    return nst.astimezone(pytz.utc)

def UTC_datetime_to_eastern(utc_datetime):
    udt = utc_datetime
    if not utc_datetime.tzinfo:
        udt = pytz.utc.localize(utc_datetime)
    eastern = pytz.timezone('US/Eastern') 
    return udt.astimezone(eastern)

def UTC_datetime_to_taipei(utc_datetime):
    udt = utc_datetime
    if not utc_datetime.tzinfo:
        udt = pytz.utc.localize(utc_datetime)
    taipei = pytz.timezone('Asia/Taipei') 
    return udt.astimezone(taipei)

def eastern_datetime_to_mysql_str(datetime):
    utc_dt = easternDatetimeToUTC(datetime)
    return str(utc_dt).replace('+00:00','')

def freq_to_timedelta(freq):
    if not freq:
        import datetime
        return datetime.timedelta(milliseconds=1)
    d = date_range('1/1/2012', periods=2, freq=freq)
    return d[1] - d[0]

def freq_to_timedelta64(freq):
    freq = freq_to_timedelta(freq)
    return np.array([freq], dtype="timedelta64[ms]")[0]

def make_every(freq):
    """
        This function returns True for every <freq>.

        freq is a datetime.timedelta.
    """
    from datetime import datetime
    def _every():
        now = datetime.now()
        if now - _every.last_call >= freq:
            _every.last_call = now
            return True
        return False
    _every.last_call = datetime.now()
    return _every

def get_gaps_in_timeseries(datetime_idx):
    if np.__version__ >= '1.7':
        diff_dt = Series(np.diff(datetime_idx.values))
    else:
        diff_dt = Series(datetime_idx.to_pydatetime()).diff()
    return diff_dt


def get_next_weekday(start):
    from datetime import timedelta
    start += timedelta(1)
    if start.weekday() > 4:
        start += timedelta(7 - start.weekday())
    return start


def get_prev_weekday(start):
    from datetime import timedelta
    start -= timedelta(1)
    if start.weekday() > 4:
        start -= timedelta(start.weekday() - 4)
    return start


def get_closest_weekday(start, forward=True):
    if start.weekday() <= 4:
        return start
    elif forward is True:
        return get_next_weekday(start)
    else:
        return get_prev_weekday(start)
