import pandas as _pd
import sys

try:
    from kyper.data._utils import get_data as _get_data
except:
    from .._utils import get_data as _get_data

_SERVICE = "ap"
_VERSION = "1.0.0"


def filter_news(start_dt=None,
                end_dt=None,
                categories=None,
                archive="latest",
                location=None,
                limit=10000):

    params = dict(
        start_dt=start_dt,
        end_dt=end_dt,
        categories=categories,
        archive=archive,
        location=location,
        limit=limit
    )
    data = _get_data(_SERVICE, _VERSION, sys._getframe().f_code.co_name, **params)

    df = _pd.read_json(data, orient="split")
    if not df.empty:
        df["published"] = _pd.to_datetime(df["published"], unit="ms")
    return df


def search_news(search_term,
                start_dt=None,
                end_dt=None,
                archive="latest",
                location=None,
                categories=None,
                offset=0,
                limit=200000,
                search_fields=["headline^2", "body"]):
    params = dict(
        key=search_term,
        start_dt=start_dt,
        end_dt=end_dt,
        archive=archive,
        location=location,
        subject=categories,
        offset=offset,
        limit=limit,
        search_fields=search_fields
    )
    data = _get_data(_SERVICE, _VERSION, sys._getframe().f_code.co_name, **params)
    df = _pd.read_json(data, orient="split")
    if not df.empty:
        df["published"] = _pd.to_datetime(df["published"], unit="ms")
    return df
