import requests
import pandas as pd
from dateutil.parser import parse


#https://www.quandl.com/api/v3/datasets/WIKI/AAPL.csv?order=asc&
#exclude_column_names=true&rows=3&start_date=2012-11-01&end_date=2013-11-30
#&column_index=4&collapse=quarterly&transform=rdiff

QUANDL_URL_BASE = 'https://www.quandl.com/api/v3/datasets/'
INPUT_DICT = {'api_key': None,
              'start_date': None,
              'end_date': None,
              'order': ['asc', 'dsc'],
              'rows': int,
              'column_index': int,
              'collapse': ['daily','weekly','monthly','quarterly','annual'],
              'transform': ['diff','rdiff','cumul']
              }

def get(dataset, ticker, **kwargs):
    url = QUANDL_URL_BASE +dataset
    url += '/' + ticker
    url += '.json?'

    if 'api_key' in kwargs:
        url += 'auth_token='+ kwargs.pop('api_key') + '&'

    kwargs = checkKwargs(**kwargs)
    url = addKwargsToUrl(url, **kwargs)
    pageJson = getPageJson(url)
    dFrame = makeDataFrame(pageJson)
    return dFrame


def checkKwargs(**kwargs):
    def checkDate(date):
        try:
            return parse(date).strftime("%Y-%m-%d")
        except ValueError as e:
            error = str(date) + " is not a valid parameter"
            raise InvalidParameter(error)

    for key, val in kwargs.iteritems():
        if key not in INPUT_DICT:
            error = str(key) + " is not a valid keyword"
            raise InvalidKeyword(error)

        if key in ['order', 'collapse','transform']:
            if val not in INPUT_DICT[key]:
                error = str(val) + " is not a valid parameter"
                raise InvalidParameter(error)

        elif key in ['rows','column_index']:
            if type(val) != INPUT_DICT[key]:
                error = str(val) + " is not int type"
                raise InvalidParameter(error)

        elif key in ['start_date','end_date']:
            kwargs[key] = checkDate(val)
    return kwargs


def addKwargsToUrl(url, **kwargs):
    for key, val in kwargs.iteritems():
        url += key + "=" + str(val) + "&"
    return url

def getPageJson(url):
    page = requests.get(url)
    return page.json()['dataset']

def makeDataFrame(pageJson):
    return pd.DataFrame(pageJson['data'], columns=pageJson['column_names'])




class InvalidKeyword(Exception):
    "Exception for Invalid Keyword"
    pass

class InvalidParameter(Exception):
    "Exception for Invalid Parameter"
    pass






