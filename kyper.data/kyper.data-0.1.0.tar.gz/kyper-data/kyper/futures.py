# -*- coding: utf-8 -*-
"""

This module is a wrapper for the Kyper futures api

Attributes:
    _VERSION (str): The Kyper api VERSION.
    _SERVICE (str): The Kyper service used in this module.

"""
from __future__ import absolute_import as _absolute_import
from future.standard_library import install_aliases as _install_aliases
from past.builtins import basestring as _basestring
_install_aliases()

import json as _json
from datetime import datetime as _datetime, timedelta as _timedelta

from dateutil.parser import parse as _parse_dt
import pandas as _pd
from tzlocal import get_localzone as _get_localzone
from kyper.util import time_helper as _time_helper
from kyper.data._utils import get_data as _get_data
# pylint: disable=E0611
# pylint: disable=F0401

_VERSION = "0.1.0"
_SERVICE = "kyper_futures"


def _parse_response_into_df(inp_string, tz='UTC'):
    """Return json as pandas.DataFrame."""
    try:
        df = _pd.read_json(inp_string, orient='split')
        return df.tz_localize('UTC').tz_convert(tz)
    except TypeError:
        return df
    except ValueError:
        return _pd.DataFrame(columns=_json.loads(inp_string)['columns'])


def get_tick_data(symbol, start_dt, end_dt, max_records=None, session_filter=None, nearby=None):
    """
|  Returns a pandas.DataFrame containing the tick data of the given symbol
   with UTC datetime as the index and ``'symbol'``, ``'tradingDay'``,
   ``'sessionCode'``, ``'tickPrice'`` and ``'tickSize'`` as the columns.

    *Note: Tick data is large. Queries spanning more than an hour (or even a
        few minutes for liquid symbols) or so during the trading day will be
        slow.*
    """
    start_dt = _parse_dt(start_dt) if isinstance(start_dt, _basestring) else start_dt
    end_dt = _parse_dt(end_dt) if isinstance(end_dt, _basestring) else end_dt

    if session_filter:
        session_filter = session_filter.replace('+', '%2B')

    response = _get_data(
        _SERVICE, 
        _VERSION,
        "get_tick_data", 
        symbol=symbol, start_dt=start_dt,
        end_dt=end_dt,
        max_records=max_records,
        session_filter=session_filter,
        nearby=nearby)

    return _parse_response_into_df(response)


def get_minute_data(symbol, start_dt, end_dt, interval=1, max_records=None, 
                        session_filter=None, nearby=None):
    """
|  Returns a pandas.DataFrame containing the minutely market data of the given
   symbol with UTC datetime as the index and ``'symbol'``,
            ``'tradingDay'``, ``'open'``, ``'high'``, ``'low'``, ``'close'``
            and ``'volume'`` as the columns.
    """
    start_dt = _parse_dt(start_dt) if isinstance(start_dt, _basestring) else start_dt
    end_dt = _parse_dt(end_dt) if isinstance(end_dt, _basestring) else end_dt

    if session_filter:
        session_filter = session_filter.replace('+', '%2B')

    response = _get_data(
        _SERVICE, 
        _VERSION, 
        "get_minute_data",
        symbol=symbol, start_dt=start_dt,
        end_dt=end_dt,
        interval=interval,
        max_records=max_records,
        session_filter=session_filter, nearby=nearby)

    return _parse_response_into_df(response)


def get_daily_data(symbol, start_date=None, end_date=None, continuous_contract=True, 
    max_records=None, session_filter=None, nearby=None):

    """
|  Returns a pandas.DataFrame containing the daily market data of the given
   symbol with UTC datetime as the index and ``'symbol'``,
            ``'tradingDay'``, ``'open'``, ``'high'``, ``'low'``, ``'close'``,
            ``'volume'`` and ``'openInterest'`` as the columns.
    """
    if session_filter:
        session_filter = session_filter.replace('+', '%2B')

    response = _get_data(
        _SERVICE, 
        _VERSION, 
        "get_daily_data",
        symbol=symbol, start_date=start_date, 
        end_date=end_date,
        continuous_contract=continuous_contract,
        max_records=max_records,
        session_filter=session_filter, nearby=nearby)

    return _parse_response_into_df(response)


def get_last_observed_price(symbol, placed_at=None, max_duration=None, vwap=False, 
                                vwap_window=_timedelta(minutes=2), session_filter=None, nearby=None):
    """
|  Returns the effective price (VWAP or last trade) immediately prior to
   ``placed_at``.

    **Parameters:**
        ``symbol`` : str
            The symbol ID to query, e.g. 'CL' or 'ES'
        ``placed_at`` : datetime.datetime, default ``None``
            The date and time at which to begin searching for a price.
            The last observed price is immediately prior to this timestamp.
            If left as ``None``, the most recent observed price at the current
            time will be retrieved.
        ``max_duration`` : datetime.timedelta, default ``None``
            The maximum time interval before ``placed_at`` to search for an
            observed price.
        ``vwap`` : bool, default ``False``
            If True, use `VWAP <http://en.wikipedia.org/wiki/Volume-weighted_average_price>`_
            to calculate the price at placed_at. VWAP will slow the query down.
            Turn this off if you just want a spot price at a time point.
        ``vwap_window`` : datetime.timedelta,
            default ``datetime.timedelta(minutes=2)``
            If ``vwap`` is True, use a time window of the specified size to
            calculate VWAP
            (extending backward from ``placed_at``)
        ``session_filter`` : str, default ``None``
            This parameter modifies the default session codes/sale conditions
            used to return ticks for each exchange. For NYSE and AMEX, the
            default session filter is "@EFKX56V9" (meaning all ticks with sale
            conditions corresponding to one of the characters in the
            filter are included in the results), for NASDAQ the default
            is "@ABDEFKOSXY156", and for everything else all session
            codes/sale conditions are returned except the settle
            (session code '*'). If the session filter is set to a string
            of valid session codes (i.e. "EFK"), only ticks with the
            specified session codes are included in the results. If the
            string is prefixed with character '!' (i.e."!EFK"), all
            session codes except those in the string are included in the
            results. If the string is prefixed with character '+'
            (i.e. "+T"), then all the default session codes in addition to
            the ones specified in the string are included in the results.
            And if the string is prefixed with character '-' (i.e. "-EF")
            then all default session codes except the ones specified are
            included in the results.
        ``nearby`` : int, default None (which is synonomous to 1)
            The offset from the front month contract.

    **Returns:**
        float, or ``None`` (if no price available prior to ``placed_at``)
    """
    if placed_at:
        placed_at = _parse_dt(placed_at) if isinstance(placed_at, _basestring) else placed_at

    if max_duration:
        max_duration = _time_helper.timedelta_to_seconds(max_duration)

    if vwap_window:
        vwap_window = _time_helper.timedelta_to_seconds(vwap_window)

    if session_filter:
        session_filter = session_filter.replace('+', '%2B')

    response = _get_data(
        _SERVICE, 
        _VERSION,
        "get_last_observed_price", 
        symbol=symbol, placed_at=placed_at,
        max_duration=max_duration, vwap=vwap,
        vwap_window=vwap_window,
        session_filter=session_filter, nearby=nearby)

    return _parse_response_into_df(response)


def is_valid_symbol(symbol):
    """
|  Determine whether a specific symbol is a valid futures contract symbol
   containing all available futures symbols with the
        following columns:

        * ``symbol``: str; the contract symbol
        * ``description``: str; contract description
        * ``exchange``: str; exchange on which the contract is traded
        * ``number``: TODO: describe ``number`` ?????
    """
    response = _get_data(_SERVICE, _VERSION,
                         "is_valid_symbol", symbol=symbol)

    return _json.loads(response)


def list_symbols():
    """
|  List all available futures contract symbols.

    **Returns:**
        A pandas.DataFrame containing all available futures symbols with the
        following columns:

        * ``symbol``: str; the contract symbol
        * ``description``: str; contract description
        * ``exchange``: str; exchange on which the contract is traded
        * ``number``: TODO: describe ``number`` ?????
    """
    response = _get_data(_SERVICE, _VERSION, "list_symbols")
    return _parse_response_into_df(response)


def search_symbols(search_term, case=False, search_cols=None):
    """
|  Search contract symbols using a keyword (str) or regular expression.

    **Parameters:**
        * ``search_term`` : str or regular expression
            The keyword or regular expression string used to search every
            value in a column (search performed through re.search()). Not case
            sensitive.
        * ``case`` : bool (default False)
            Indicates whether search is case sensitive or not (ie True is
            case sensitive).
        * ``search_cols`` : str, list of str, int, list of int
            Indicates which columns to search through. Valid values are:
            a column name (str), a column index (int), or a list of column
            names or indexes.

    **Returns:**
        A pandas.DataFrame containing search results with the following columns:

        * ``symbol``: str; the contract symbol
        * ``description``: str; contract description
        * ``exchange``: str; exchange on which the contract is traded
        * ``number``: TODO: describe ``number`` ?????
    """
    response = _get_data(
        _SERVICE, 
        _VERSION, 
        "search_symbols",
        search_term=search_term, case=case,
        search_cols=search_cols)

    return _parse_response_into_df(response)
