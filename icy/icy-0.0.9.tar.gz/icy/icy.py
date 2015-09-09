"""
icy
---
data wrangling glue code
"""

import os
import sys
import zipfile
import pandas as pd
import numpy as np
import yaml
from datetime import datetime
from copy import deepcopy

examples = {
    'artists': ('local/artists.zip', 'local/artists_read.yml', {}),
    'babynames': ('local/babynames.zip', 'local/babynames_read.yml', {}),
    'bank': ('local/bank.zip', 'local/bank_read.yml', {}),
    'caterpillar': ('local/caterpillar.zip', 'local/caterpillar_read.yml', {}),
    'churn': ('local/churn.zip', 'local/churn_read.yml', {}),
    'comunio': ('local/comunio', {}, {}),
    'crossdevice': ('local/crossdevice.zip', {}, {}),
    'egg': ('local/egg', 'local/egg_read.yml', {}),
    # 'fed': ('local/fed.zip', {}, {}),
    'formats': ('local/formats', {}, {}),
    'lahman': ('local/lahman.zip', 'local/lahman_read.yml', {}),
    'nyse1': ('local/nyse_1.zip', 'local/nyse_1_read.yml', {}),
    'nyse2': ('local/nyse_2.tsv.gz', 'local/nyse_2_read.yml', {}),
    'nyt_title': ('local/nyt_title.zip', 'local/nyt_title_read.yml', {}),
    'otto': ('local/otto.zip', {}, {}),
    'spam': ('local/sms_spam.zip', 'local/sms_spam_read.yml', {}),
    'titanic': ('local/titanic.zip', {}, {}),
    'wikipedia': ('local/wikipedia_langs.zip', 'local/wikipedia_read.yml', {})
}

def to_df(obj, cfg={}, raise_on_error=True, silent=False, verbose=False):
    if type(obj) == str:
        name = obj
    else:
        name = obj.name
    name = name[name.rfind('/') + 1:]
    
    if not raise_on_error:
        try:
            return to_df(obj=obj, cfg=cfg, raise_on_error=True)
        except (pd.parser.CParserError, AttributeError) as e:
            if not silent:
                print('WARNING in {}: {}'.format(name, e))
            return None
        except:
            if not silent:
                print('WARNING in {}: {}'.format(name, sys.exc_info()[0]))
            return None
    
    params = {}
    if 'default' in cfg:
        params = deepcopy(cfg['default'])
    if name in cfg:
        for e in cfg[name]:
            params[e] = deepcopy(cfg[name][e])
    if 'custom_date_parser' in params:
        params['date_parser'] = DtParser(params['custom_date_parser']).parse
        del params['custom_date_parser']
    
    if not silent and verbose:
        print(name, params)
    
    if name.startswith('s3:'):
        try:
            import boto
        except:
            raise ImportError('reading from aws-s3 requires the boto package to be installed')
    
    if '.csv' in name:
        # name can be .csv.gz, .csv.bz2 or similar
        return pd.read_csv(obj, **params)
        
    elif '.tsv' in name or '.txt' in name:
        # name can be .tsv.gz, .txt.bz2 or similar
        return pd.read_table(obj, **params)
    
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
    
    elif name.endswith(('.xls', '.xlsx')):
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
            for key in store.keys():
                data[key[1:]] = store[key]
        return data
    
    elif name.endswith(('.sqlite', '.sql')):
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

def read(path, cfg={}, filters=[], raise_on_error=False, silent=False):
    """Dictionary of pandas.DataFrames
    
    Parameters
    ----------
    path : str
        Location of folder, zip-file or file to be parsed.
        Can be remote with URI-notation like http:, https:, file:, ftp: and s3:.
        Parser will be selected based on file extension.
    filters : str or list of strings, optional
        For a file to be processed, it must contain one of the Strings (e.g. ['.csv', '.tsv'])
    cfg : dict or str, optional
        Dictionary of kwargs to be provided to the pandas.io parser
        or str with path to YAML, that will be parsed.
        
        Special keys:
        
        **filters** : set filters-parameter from config
        
        **default** : kwargs to be used for every file
        
        **custom_date_parser** : strptime-format string (https://docs.python.org/3.4/library/datetime.html#strftime-strptime-behavior), generates a parser that used as the *date_parser* argument
        
        If filename in keys, use kwargs from that key in addition to or overwriting *default* kwargs.
    raise_on_error : boolean
        Raise exception or only display warning, if a file cannot be parsed successfully
        
    Returns
    -------
    data : dict
        Dictionary of parsed pandas.DataFrames, with file names as keys
    
    Notes
    -----
    - Start with basic cfg and tune until the desired parsing result is achieved
    - Make sure file extensions are descriptive
    - Avoid files named 'default'
    - Avoid duplicate file names
    - Subfolders and file names beginning with '.' or '_' are ignored
    - If an https:// URI isn't correctly processed, try http:// instead
    """
    
    if type(filters) == str:
        filters = [filters]
    if type(cfg) == str:
        yml = read_cfg(cfg)
        if yml == None:
            if not silent:
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
    errors = []
    
    if not silent:
        print('processing', path, '...')
    
    if os.path.isdir(path):
        # path is folder
        files = []
        for e in os.listdir(path):
            if os.path.isfile(os.path.join(path, e)):
                if e[0] not in ['.', '_']:
                    if filters == []:
                        files.append(e)
                    else:
                        if any(f in e for f in filters):
                            files.append(e)
        for fn in files:
            result = read(path=os.path.join(path, fn), cfg=cfg, filters=filters, \
                raise_on_error=raise_on_error, silent=silent)
            
            key = fn[fn.rfind('/') + 1:]
            if type(result) == dict:
                if len(result) == 0:
                    errors.append(key)
                elif len(result) == 1:
                    r = next(iter(result))
                    data[r] = result[r]
                else:
                    for r in result:
                        data['_'.join([key, r])] = result[r]
            elif type(result) == type(None):
                errors.append(key)
            else:
                data[key] = result
    
    elif os.path.isfile(path):
        # path is file

        if zipfile.is_zipfile(path) and not path.endswith(('.xlsx', '.xls')):
            # path is zipfile
            # !identifies xlsx as archive of xml files
            
            with zipfile.ZipFile(path) as myzip:
                files = []
                for e in myzip.namelist():
                    # ignore hidden / system files and folders
                    if e[0] not in ['.', '_'] and e[-1] not in ['/']:
                        if filters == []:
                            files.append(e)
                        else:
                            if any(f in e for f in filters):
                                files.append(e)
                for fn in files:
                    with myzip.open(fn) as file:
                        data, errors = _read_append(data=data, errors=errors, path=file, fname=fn, \
                            cfg=cfg, raise_on_error=raise_on_error, silent=silent)
        
        else:
            # path is other file
            data, errors = _read_append(data=data, errors=errors, path=path, fname=path, \
                cfg=cfg, raise_on_error=raise_on_error, silent=silent)
    
    elif path.startswith(('http:', 'https:', 'ftp:', 's3:', 'file:')):
        # path is in url-/uri-notation
        data, errors = _read_append(data=data, errors=errors, path=path, fname=path, \
            cfg=cfg, raise_on_error=raise_on_error, silent=silent)

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
    
    if not silent:
        print('imported {} DataFrames'.format(len(data)))
        if len(data) > 0:
            print('total memory usage: {}'.format(mem(data)))
        if len(errors) > 0:
            print('import errors in files: {}'.format(', '.join(errors)))
    return data

def _read_append(data, errors, path, fname, cfg, raise_on_error, silent):
    key = fname[fname.rfind('/') + 1:]
    result = to_df(obj=path, cfg=cfg, raise_on_error=raise_on_error, silent=silent)
    if type(result) == dict:
        if len(result) == 0:
            errors.append(key)
        elif len(result) == 1:
            r = next(iter(result))
            data[r] = result[r]
        else:
            for r in result:
                data['_'.join([key, r])] = result[r]
    elif type(result) == type(None):
        errors.append(key)
    else:
        data[key] = result
    return data, errors

def preview(path, cfg={}, filters=[], rows=5):
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
        
    if type(cfg) != dict:
        cfg = {'default': {'nrows': rows}}
    else:
        if 'default' in cfg:
            if type(cfg['default']) == dict:
                cfg['default']['nrows'] = rows
            else:
                cfg['default'] = {'nrows': rows}
        else:
            cfg['default'] = {'nrows': rows}
    prev = read(path=path, cfg=cfg, filters=filters, silent=True)

    structure = {}
    for key in sorted(prev):
        print('File: {}'.format(key))
        print()
        prev[key].info(verbose=True, memory_usage=True, null_counts=True)
        print()
        print('{:<20} | first {} VALUES'.format('COLUMN', rows))
        print('-'*40)
        structure[key] = {}
        for col in prev[key].columns:
            print('{:<20} | {}'.format(col, str(list(prev[key][col].values))))
            structure[key][col] = list(prev[key][col].values)
        print('='*40)

    print('Successfully parsed first {} rows of {} files:'.format(rows, len(prev)))
    print(', '.join(sorted(prev)))
    # structure -> yaml ?
    return
    
def mem(data):
    """Total memory used by data
    
    Parameters
    ----------
    data : dict of pandas.DataFrames or pandas.DataFrame
    
    Returns
    -------
    str : str
        Human readable amount of memory used with unit (like KB, MB, GB etc.)
    """
    
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

def _dtparse(s, pattern):
    return datetime.strptime(s, pattern)

class DtParser():
    def __init__(self, pattern):
        self.pattern = pattern
        self.vfunc = np.vectorize(_dtparse)
        
    def parse(self, s):
        if type(s) == str:
            return _dtparse(s, self.pattern)
        elif type(s) == list:
            return [_dtparse(e, self.pattern) for e in s]
        elif type(s) == np.ndarray:
            return self.vfunc(s, self.pattern)
