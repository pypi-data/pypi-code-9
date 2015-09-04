#!/usr/bin/env python3
# -*- coding: utf8 -*-
from __future__ import absolute_import as _absolute_import
from future.standard_library import install_aliases as _install_aliases
from past.builtins import basestring as _basestring
_install_aliases()

import pandas as _pd
import json as _json
from kyper.data._utils import get_data as _get_data
 
_VERSION = "0"
_SERVICE = "wikidata"

# TODO: we'll also need to better understand pages/searches/objects returned (not all are Wikipedia)
# NOTE: will likely need additional util function to assist w/ groupby transformations


def find(search_term, start_dt=None, end_dt=None, lang='en', freq='h'):
    """ find Wiki Page Counts statistics with specified keywords

    :param search_term str,list: The keyword or keywords to search for
    :param start_dt str,datetime.date,datetiem.datetime: The optional start date for the query (optional). If this value is not specified, it will be the same time NOW in yesterday
    :param end_dt str,datetime.date,datetiem.datetime: The optional end date for the query (optional). If this value is not specified, it will be NOW
    :param lang str: The optional for the language (default: 'en')
    :param freq str: The returned Wiki Page Counts frequence, can be one of 'h', 'd', 'w', 'm', which stand for hourly, daily, weekly and monthly

    :ret pandas.DataFrame: Return a pandas DataFrame contains Wiki Page Counts statistics with specified keywords
    """
    start_dt = _parse_dt(start_dt) if isinstance(start_dt, _basestring) else start_dt
    end_dt = _parse_dt(end_dt) if isinstance(end_dt, _basestring) else end_dt

    search_term = _json.dumps(search_term)
    ret = _get_data(_SERVICE, _VERSION, "find", search_term=search_term,
            start_time=start_dt, end_time=end_dt, lang=lang, freq=freq)
    return _pd.read_json(ret, orient="split")

'''def text_search(search_term, start_time=None, end_time=None, lang='en', freq='h'):
    """ Get Wiki Page Counts statistics in which title contains keywords.

    :param search_term str: The single keyword to search for (required)
    :param start_time str,datetime.date,datetiem.datetime: The optional start date for the query (optional). If this value is not specified, it will be the same time NOW in yesterday
    :param end_time str,datetime.date,datetiem.datetime: The optional end date for the query (optional). If this value is not specified, it will be NOW
    :param lang str: The optional for the language (default: 'en')
    :param freq str: The returned Wiki Page Counts frequence, can be one of 'h', 'd', 'w', 'm', which stand for hourly, daily, weekly and monthly

    :ret pandas.DataFrame: Return a pandas DataFrame contains Wiki Page Counts statistic in which title contains keywords. The index datetime means the latest time the search_term was found and accumulated in the time period of freq
    """
    search_term = _json.dumps(search_term)
    ret = _get_data(_SERVICE, _VERSION, "textSearch", search_term=search_term,
            start_time=start_time, end_time=end_time, lang=lang, freq=freq)
    return _pd.read_json(ret, orient="split")'''


def lang():
    """Get Wikipedia.org languages

    :ret pandas.DataFrame: Return a pandas DataFrame contains all languages of Wikipedia.org.
    """
    ret = _get_data(_SERVICE, _VERSION, "lang")
    return _pd.read_json(ret, orient="split")

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
