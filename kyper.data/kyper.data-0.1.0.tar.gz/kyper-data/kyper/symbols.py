# -*- coding: utf-8 -*-
from future.standard_library import install_aliases as _install_aliases
_install_aliases()

import json as _json
from datetime import timedelta as _timedelta
import pandas as _pd
from kyper.util import time_helper as _time_helper
from kyper.data._utils import get_data as _get_data

_VERSION = "0"
_SERVICE = "kyper_symbols"

def _parse_response_into_df(js):
    try:
        df = _pd.read_json(js, orient='split')
        return df.tz_localize('UTC')
    except TypeError:
        return df #pd.read_json(js, orient='split')
    except ValueError:
        return _pd.DataFrame(columns=json.loads(js)['columns'])


def is_valid_symbol(symbol, asset_class=None):
    """
|  Determine whether a specific symbol is a valid symbol within a specific asset class.

    **Parameters:** 
        * ``symbol`` : str
            The symbol to be tested for validity.
 
    **Returns:** 
        A DataFrame containing all available symbols with the following columns:

        * ``symbol``: str; the instrument symbol
        * ``description``: str; instrument description
        * ``exchange``: str; exchange on which the instrument is traded
        * ``number``: TODO: describe ``number`` ?????
    """

    response = _get_data(
        _SERVICE, 
        _VERSION, 
        "is_valid_symbol", 
        symbol=symbol, asset_class=asset_class)

    return _json.loads(response)

 
def is_valid_futures_symbol(symbol):
    """
|  Determine whether a specific symbol is a valid futures contract symbol.

    **Parameters:** 
        * ``symbol`` : str
            The symbol to be tested for validity.
 
    **Returns:** 
        A DataFrame containing all available futures symbols with the following columns:

        * ``symbol``: str; the contract symbol
        * ``description``: str; contract description
        * ``exchange``: str; exchange on which the contract is traded
        * ``number``: TODO: describe ``number`` ?????
    """

    response = _get_data(
        _SERVICE, 
        _VERSION, 
        "is_valid_futures_symbol", 
        symbol=symbol)

    return _json.loads(response)
  
 
def is_valid_equities_symbol(symbol):
    """
|  Determine whether a specific symbol is a valid U.S. equity ticker symbol.

    **Parameters:** 
        * ``symbol`` : str
            The symbol to be tested for validity.
 
    **Returns:** 
        A DataFrame containing all available U.S. equities ticker symbols with the following columns:

        * ``symbol``: str; the instrument symbol
        * ``description``: str; instrument description
        * ``exchange``: str; exchange on which the instrument is traded
        * ``number``: TODO: describe ``number`` ?????
    """

    response = _get_data(
        _SERVICE, 
        _VERSION, 
        "is_valid_equities_symbol", 
        symbol=symbol)

    return _json.loads(response)
  

def is_valid_index_symbol(symbol):
    """
|  Determine whether a specific symbol is a valid index symbol.

    **Parameters:** 
        * ``symbol`` : str
            The symbol to be tested for validity.
 
    **Returns:** 
        A DataFrame containing all available index symbols with the following columns:

        * ``symbol``: str; the instrument symbol
        * ``description``: str; instrument description
        * ``exchange``: str; exchange on which the instrument is traded
        * ``number``: TODO: describe ``number`` ?????
    """

    response = _get_data(
        _SERVICE, 
        _VERSION, 
        "is_valid_index_symbol", 
        symbol=symbol)

    return _json.loads(response)
 

def list_symbols(asset_class):
    """
|  List all available instrument symbols by asset class.

    **Returns:** 
        A DataFrame containing all available futures symbols with the following columns:

        * ``symbol``: str; the contract symbol
        * ``description``: str; contract description
        * ``exchange``: str; exchange on which the contract is traded
        * ``number``: TODO: describe ``number`` ?????
    """

    response = _get_data(
        _SERVICE, 
        _VERSION, 
        "list_symbols",
        asset_class=asset_class)

    df = _parse_response_into_df(response)

    return df
 

def list_futures_symbols():
    """
|  List all available futures contract symbols.

    **Returns:** 
        A DataFrame containing all available futures symbols with the following columns:

        * ``symbol``: str; the contract symbol
        * ``description``: str; contract description
        * ``exchange``: str; exchange on which the contract is traded
        * ``number``: TODO: describe ``number`` ?????
    """

    response = _get_data(
        _SERVICE, 
        _VERSION, 
        "list_futures_symbols")

    df = _parse_response_into_df(response)

    return df
 

def list_equities_symbols():
    """
|  List all available U.S. equities ticker symbols.

    **Returns:** 
        A DataFrame containing all available U.S. equities ticker symbols with the following columns:

        * ``symbol``: str; the instrument symbol
        * ``description``: str; instrument description
        * ``exchange``: str; exchange on which the instrument is traded
        * ``number``: TODO: describe ``number`` ?????
    """

    response = _get_data(
        _SERVICE, 
        _VERSION, 
        "list_equities_symbols")

    df = _parse_response_into_df(response)

    return df


def list_index_symbols():
    """
|  List all available index symbols.

    **Returns:** 
        A DataFrame containing all available index symbols with the following columns:

        * ``symbol``: str; the instrument symbol
        * ``description``: str; instrument description
        * ``exchange``: str; exchange on which the instrument is traded
        * ``number``: TODO: describe ``number`` ?????
    """

    response = _get_data(
        _SERVICE, 
        _VERSION, 
        "list_index_symbols")

    df = _parse_response_into_df(response)

    return df
 
 
def search_symbols(search_term, asset_class, case=False, search_cols=None):
    """
|  Search instrument symbols within an asset class using a keyword or regular expression.

    **Parameters:** 
        * ``search_term`` : str or regular expression str
            The keyword or regular expression string used to search every
            value in a column (search performed through re.search()).
        * ``case`` : bool (default False)
            Indicates whether search is case sensitive or not (ie True is case sensitive).
        * ``search_cols`` : str, list of str, int, list of int
            Indicates which columns to search through. Valid values are:
            a column name (str), a column index (int), or a list of column names or indexes.

    **Returns:** 
        A DataFrame containing positive search results with the following columns:

        * ``symbol``: str; the instrument symbol
        * ``description``: str; instrument description
        * ``exchange``: str; exchange on which the instrument is traded
        * ``number``: TODO: describe ``number`` ?????
    """

    response = _get_data(
        _SERVICE, 
        _VERSION, 
        "search_symbols", 
        search_term=search_term, asset_class=asset_class,
        case=case, search_cols=search_cols)

    df = _parse_response_into_df(response)
    return df

 
def search_futures_symbols(search_term, case=False, search_cols=None):
    """
|  Search futures contract symbols using a keyword or regular expression.

    **Parameters:** 
        * ``search_term`` : str or regular expression str
            The keyword or regular expression string used to search every
            value in a column (search performed through re.search()).
        * ``case`` : bool (default False)
            Indicates whether search is case sensitive or not (ie True is case sensitive).
        * ``search_cols`` : str, list of str, int, list of int
            Indicates which columns to search through. Valid values are:
            a column name (str), a column index (int), or a list of column names or indexes.

    **Returns:** 
        A DataFrame containing positive search results with the following columns:

        * ``symbol``: str; the instrument symbol
        * ``description``: str; instrument description
        * ``exchange``: str; exchange on which the instrument is traded
        * ``number``: TODO: describe ``number`` ?????
    """

    response = _get_data(
        _SERVICE, 
        _VERSION, 
        "search_futures_symbols", 
        search_term=search_term, case=case, search_cols=search_cols)

    df = _parse_response_into_df(response)
    return df

 
def search_equities_symbols(search_term, case=False, search_cols=None):
    """
|  Search U.S equities ticker symbols using a keyword or regular expression.

    **Parameters:** 
        * ``search_term`` : str or regular expression str
            The keyword or regular expression string used to search every
            value in a column (search performed through re.search()).
        * ``case`` : bool (default False)
            Indicates whether search is case sensitive or not (ie True is case sensitive).
        * ``search_cols`` : str, list of str, int, list of int
            Indicates which columns to search through. Valid values are:
            a column name (str), a column index (int), or a list of column names or indexes.

    **Returns:** 
        A DataFrame containing positive search results with the following columns:

        * ``symbol``: str; the instrument symbol
        * ``description``: str; instrument description
        * ``exchange``: str; exchange on which the instrument is traded
        * ``number``: TODO: describe ``number`` ?????
    """

    response = _get_data(
        _SERVICE, 
        _VERSION, 
        "search_equities_symbols", 
        search_term=search_term, case=case, search_cols=search_cols)

    df = _parse_response_into_df(response)
    return df

 
def search_index_symbols(search_term, case=False, search_cols=None):
    """
|  Search index instrument symbols using a keyword or regular expression.

    **Parameters:** 
        * ``search_term`` : str or regular expression str
            The keyword or regular expression string used to search every
            value in a column (search performed through re.search()).
        * ``case`` : bool (default False)
            Indicates whether search is case sensitive or not (ie True is case sensitive).
        * ``search_cols`` : str, list of str, int, list of int
            Indicates which columns to search through. Valid values are:
            a column name (str), a column index (int), or a list of column names or indexes.

    **Returns:** 
        A DataFrame containing positive search results with the following columns:

        * ``symbol``: str; the instrument symbol
        * ``description``: str; instrument description
        * ``exchange``: str; exchange on which the instrument is traded
        * ``number``: TODO: describe ``number`` ?????
    """

    response = _get_data(
        _SERVICE, 
        _VERSION, 
        "search_index_symbols", 
        search_term=search_term, case=case, search_cols=search_cols)

    df = _parse_response_into_df(response)
    return df


