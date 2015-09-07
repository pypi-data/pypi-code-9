"""
icy
---
data wrangling glue code
"""

import os
import zipfile
import pandas as pd
import yaml
from copy import deepcopy

examples = {
    'artists': 'local/artists.zip',
    'babynames': 'local/babynames.zip',
    'bank': 'local/bank.zip',
    'caterpillar': 'local/caterpillar.zip',
    'churn': 'local/churn.zip',
    'comunio': 'local/comunio',
    'crossdevice': 'local/crossdevice.zip',
    'egg': 'local/egg',
    'formats': 'local/formats',
    'lahman': 'local/lahman.zip',
    'nyse1': 'local/nyse_1.zip',
    'nyse2': 'local/nyse_2.tsv.gz',
    'nyt_title': 'local/nyt_title.zip',
    'otto': 'local/otto.zip',
    'spam': 'local/sms_spam.zip',
    'titanic': 'local/titanic.zip',
    'wikipedia': 'local/wikipedia_langs.zip'
}

def to_df(obj, cfg={}, raise_on_error=True):
    if type(obj) == str:
        name = obj
    else:
        name = obj.name
    if not raise_on_error:
        try:
            return to_df(obj, cfg, raise_on_error=True)
        except (pd.parser.CParserError, AttributeError) as e:
            print('WARNING in {}: {}'.format(name, e))
            return None
        except:
            print('WARNING in {} other Error'.format(name))
    params = {}
    if 'default' in cfg:
        params = deepcopy(cfg['default'])
    if name in cfg:
        for e in cfg[name]:
            params[e] = deepcopy(cfg[name][e])
    if '.csv' in name or '.tsv' in name or '.txt' in name:
        # name can be .csv.gz, .tsv.bz2 or similar:
        if '.tsv' in name:
            if 'sep' not in params:
                params['sep'] = '\t'
        return pd.read_csv(obj, **params)
    elif name.endswith('.htm') or name.endswith('.html') or name.endswith('.xml'):
        try:
            import lxml
        except:
            params['flavor'] = 'bs4'
            try:
                import bs4
                import html5lib
            except:
                raise ImportError('reading html/xml requires the lxml or bs4 + html5lib packages to be installed')
        data = pd.read_html(obj, **params)
        data = {str(i): data[i] for i in range(len(data))}
        return data
    elif name.endswith('.json'):
        return pd.read_json(obj, **params)
    elif name.endswith('.xls') or name.endswith('.xlsx'):
        try:
            import xlrd
        except:
            raise ImportError('reading excel files requires the xlrd package to be installed')
        data = {}
        xls = pd.ExcelFile(obj)
        for key in xls.sheet_names:
            data[key] = xls.parse(key, **params)
        return data
    elif name.endswith('.h5'):
        try:
            import tables
        except:
            raise ImportError('reading hdf5 files requires the pytables package to be installed')
        with pd.HDFStore(obj) as store:
            data = {}
            for key in store:
                data[key[1:]] = store[key]
        return data
    elif name.endswith('.sqlite') or name.endswith('.sql'):
        import sqlite3
        if type(obj) != str:
            raise IOError('sqlite-database must be decompressed before import')
        with sqlite3.connect(obj) as con:
            data = {}
            cursor = con.cursor()
            cursor.execute('SELECT name FROM sqlite_master WHERE type="table"')
            tables = [t[0] for t in cursor.fetchall()]
            for t in tables:
                sql = 'SELECT * FROM ' + t
                data[t] = pd.read_sql_query(sql, con, **params)
        return data
    else:
        raise AttributeError('Error creating DataFrame from object')
    
def read(path, filters=[], cfg={}, raise_on_error=False):
    """Dictionary of pandas.DataFrames
    
    Parameters
    ----------
    path : str
        Location of folder, zip-file or file to be parsed.
        Parser will be selected based on file extension.
    filters : str or list of strings, optional
        For a file to be processed, it must contain one of the Strings (e.g. ['.csv', '.tsv'])
    cfg : dict or str, optional
        Dictionary of kwargs to be provided to the pandas.io parser
        or str with path to YAML, that will be parsed.
        Special keys:
            'filters' : set filters-parameter from config
            'default' : kwargs to be used for every file
        If filename in keys, use kwargs from that key in addition to default kwargs.
    raise_on_error : boolean
        Raise exception or only display warning, if a file cannot be parsed successfully
        
    Returns
    -------
    dict
        Dictionary of parsed pandas.DataFrames, with file names as keys
    
    Notes
    -----
    - Start with basic cfg and tune until the desired parsing result is achieved
    - Make sure file extensions are descriptive
    - Avoid files named 'default'
    - Avoid duplicate file names
    - Subfolders and file names beginning with '.' or '_' are ignored
    """
    
    if type(filters) == str:
        filters = [filters]
    if type(cfg) == str:
        yml = read_cfg(cfg)
        if yml == None:
            print('creating read.yml config file draft ...')
            cfg = {'filters': ['.csv'], 'default': {'sep': ',', 'parse_dates': []}}
            with open('local/read.yml', 'w') as f:
                yaml.dump(cfg, f)
            yml = read_cfg('local/read.yml')
        if filters == [] and 'filters' in yml:
            filters = yml['filters']
            if type(filters) == str:
                filters = [filters]
            del yml['filters']
        cfg = yml
    data = {}

    print('processing', path, '...')

    if os.path.isdir(path):
        # path is folder
        files = []
        for e in os.listdir(path):
            if os.path.isfile(os.path.join(path, e)):
                if not e.startswith('.'):
                    if filters == []:
                        files.append(e)
                    else:
                        if any(f in e for f in filters):
                            files.append(e)
        for fn in files:
            if '/' in fn:
                key = fn.rsplit('/', 1)[1]
            else:
                key = fn
            result = read(os.path.join(path, fn), filters, cfg, raise_on_error)
            if type(result) == dict:
                for r in result:
                    data['_'.join([key,r])] = result[r]
            elif type(result) == type(None):
                pass
            else:
                data[key] = result
    
    elif os.path.isfile(path):
        # path is file
        if path.endswith('.sql') or path.endswith('.sqlite') \
            or path.endswith('.xlsx') or path.endswith('.xls') \
            or path.endswith('.gz') or path.endswith('.bz2'):
            print('processing file ...')
            # these mustn't be openend before calling to_df()
            if '/' in path:
                key = path.rsplit('/', 1)[1]
            else:
                key = path
            result = to_df(path, cfg, raise_on_error)
            if type(result) == dict:
                for r in result:
                    data['_'.join([key, r])] = result[r]
            elif type(result) == type(None):
                pass
            else:
                data[key] = result
        else:
            if zipfile.is_zipfile(path):
                # path is zipfile
                # !identifies xlsx as archive of xml files
                with zipfile.ZipFile(path) as myzip:
                    files = []
                    for e in myzip.namelist():
                        # ignore hidden / system files
                        if e[0] not in ['.', '_'] and e[-1] not in ['/']:
                            if filters == []:
                                files.append(e)
                            else:
                                if any(f in e for f in filters):
                                    files.append(e)
                    for fn in files:
                        with myzip.open(fn) as file:
                            if '/' in fn:
                                key = fn.rsplit('/', 1)[1]
                            else:
                                key = fn
                            result = to_df(file, cfg, raise_on_error)
                            if type(result) == dict:
                                for r in result:
                                    data['_'.join([key,r])] = result[r]
                            elif type(result) == type(None):
                                pass
                            else:
                                data[key] = result
            else:
                # not a folder
                # not a file that may not be opened before calling to_df()
                # not a zipfile
                with open(path) as file:
                    if '/' in path:
                        key = path.rsplit('/', 1)[1]
                    else:
                        key = path
                    result = to_df(file, cfg, raise_on_error)
                    if type(result) == dict:
                        for r in result:
                            data['_'.join([key,r])] = result[r]
                    elif type(result) == type(None):
                        pass
                    else:
                        data[key] = result
    else:
        try:
            import sqlalchemy
            if type(path) == sqlalchemy.engine:
                raise NotImplemented('SQLAlchemy support is not yet available')
        except ImportError:
            pass
        try:
            import pymongo
            if type(path) == pymongo.MongoClient():
                raise NotImplemented('pymongo support is not yet available')
        except ImportError:
            pass
        try:
            import elasticsearch
            if type(path) == elasticsearch.Elasticsearch():
                raise NotImplemented('elasticsearch support is not yet available')
        except ImportError:
            pass
        raise AttributeError('path must be valid file, folder or zip-archive')
    
    print('imported {} DataFrames'.format(len(data.keys())))
    if len(data.keys()) > 0:
        print('total memory usage: {}'.format(mem(data)))
    return data

def mem(data):
    if type(data) == dict:
        num = sum([data[k].memory_usage(index=True).sum() for k in data])
    else:
        num = data.memory_usage(index=True).sum()
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0
    return "%3.1f %s" % (num, 'PB')

def read_cfg(path):
    if os.path.exists(path):
        with open(path) as f:
            return yaml.safe_load(f)
    else:
        return None
    
def merge(data, cfg=None):
    """ WORK IN PROGRESS
    Concat, merge, join, drop keys in dictionary of pandas.DataFrames
    into one pandas.DataFrame (data) and a pandas.Series (labels)
    
    Parameters
    ----------
    data : dict of pandas.DataFrames
        Result of icy.read()
    cfg : dict or str, optional
        Dictionary of actions to perform on data
        or str with path to YAML, that will be parsed.
    
    Returns
    -------
    data : pandas.DataFrame
        The aggregated dataset
    labels : pandas.Series
        The target variable for analysis of the dataset,
        can have fewer samples than the aggregated dataset
    
    Notes
    -----
    
    """
    
    # go from a dict of dataframes (data) to one dataframe (data) and one series (labels)
    # pd.concat([df1, df2], join, join_axes, ignore_index) and pd.merge(left, right, how, on, suffixes)
    # should be easy to iterate from normalized tables to a fully joined set of dataframes
    
    if type(cfg) == str:
        cfg = read_cfg(cfg)
    if cfg == None:
        cfg = read_cfg('local/merge.yml')
        if cfg == None:
            print('creating merge.yml config file draft ...')
            cfg = {}
            # find all tables with identical column names
            # if no common key-col
            # concat along rows, add col (src)
            # e.g. chimps
            
            # find all tables with same length
            # if no duplicate column names
            # concat along columns
            
            # find master table (by length?)
            # from smalles to biggest table
            # find possible key-cols by uniques == len
            # find bigger tables with common column names -> cands
            # check for highest overlap-ratio of uniques -> cand (prefer smaller table if equal ratio)
            # join table on best cand
            # if ratio below treshold put table on unidentified list

            for key in data:
                cfg[key] = list(data[key].columns)
            with open('local/merge.yml', 'w') as f:
                yaml.dump(cfg, f)
            cfg = read_cfg('local/merge.yml')
    
    # if cfg == None:
    #     if not os.path.exists(default_cfg):
    #         create default_cfg draft
    #     else:
    #         join on default_cfg
    #         report join_result
    # else:
    #     join on cfg
    #     report join_result
    
    labels = None
    return data, labels

def key_cols(df):
    keys = []
    for col in df:
        if len(df[col].unique()) == len(df[col]):
            keys.append(col)
    return keys
