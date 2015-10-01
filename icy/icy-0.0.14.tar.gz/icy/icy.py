"""
icy: Python 3 data wrangling glue code
--------------------------------------
saving time handling multiple different data sources
"""

import os
import sys
import re
import zipfile
import pandas as pd
import numpy as np
import yaml
from odo import odo
from glob import glob
from fnmatch import fnmatch
from datetime import datetime
from copy import deepcopy
from itertools import chain
from importlib.util import find_spec

examples = {
    'artists': ('artists.zip', 'artists_read.yml', {}),
    'babynames': ('babynames.zip', 'babynames_read.yml', {}),
    'bank': ('bank.zip', 'bank_read.yml', {}),
    'caterpillar': ('caterpillar.zip', 'caterpillar_read.yml', {}),
    'churn': ('churn.zip', 'churn_read.yml', {}),
    'comunio': ('comunio', {}, {}),
    'crossdevice': ('crossdevice.zip', {}, {}),
    'crunchbase': ('crunchbase', {}, {}),
    'egg': ('egg', 'egg_read.yml', {}),
    # 'fed': ('fed.zip', {}, {}),
    'formats': ('formats', {}, {}),
    'lahman': ('lahman.zip', 'lahman_read.yml', {}),
    'nyse1': ('nyse_1.zip', 'nyse_1_read.yml', {}),
    'nyse2': ('nyse_2.tsv.gz', 'nyse_2_read.yml', {}),
    'nyt_title': ('nyt_title.zip', 'nyt_title_read.yml', {}),
    'otto': ('otto.zip', {}, {}),
    'spam': ('sms_spam.zip', 'sms_spam_read.yml', {}),
    'titanic': ('titanic.zip', {}, {}),
    'wikipedia': ('wikipedia_langs.zip', 'wikipedia_read.yml', {})
}

def _path_to_objs(path, include=['*', '.*'], exclude=['.*', '_*']):
    """Turn path with opt. globbing into valid list of files respecting
    include and exclude patterns.
    
    Parameters
    ----------
    path : str
        Path to process. Can be location of a file, folder or glob.
        Can be in uri-notation, can be relative or absolute or start with ~.
    include : list, optional
        Globbing patterns to require in result, defaults to ['*', '.*'].
    exclude : list, optional
        Globbing patterns to exclude from result, defaults to ['.*', '_*'].
    
    Returns
    -------
    objs : list
        List of valid files
    
    Notes
    -----
    - Doesn't show hidden files starting with '.' by default. To enable hidden files, make sure '.*' is in `include` and '.*' is not in `exclude`.
    - Doesn't show files starting with '_' by default. To enable these files, make sure '_*' is not in `exclude`.
    """
    
    if '://' in path:
        # don't modify when path is in uri-notation, except for local files
        if path.startswith('file://'):
            path = path[7:]
        else:
            return [path]
    
    path = os.path.abspath(os.path.expanduser(path))
    
    if os.path.isfile(path):
        if not path.lower().endswith(('.xlsx', '.xls')) and zipfile.is_zipfile(path):
            # zipfile misidentifies xlsx as archive of xml files
            with zipfile.ZipFile(path) as myzip:
                zipped = []
                for z in myzip.namelist():
                    z_fn = os.path.basename(z)
                    if z_fn != '' and any([fnmatch(z_fn, i) for i in include]) and \
                        not any([fnmatch(z_fn, e) for e in exclude]):
                        zipped.append(z)
                return [myzip.open(z) for z in zipped]
        else:
            return [path]
    elif os.path.isdir(path):
        cands = [os.path.abspath(os.path.join(path, p)) for p in os.listdir(path)]
        dirname = path
    else:
        cands = []
        dirname = os.path.dirname(path)
    
    include = list(chain.from_iterable(glob(os.path.join(dirname, i)) for i in include))
    exclude = list(chain.from_iterable(glob(os.path.join(dirname, e)) for e in exclude))
    
    objs = []
    if cands == []:
        cands = glob(path)
    for p in cands:
        if os.path.isfile(p) and p in include and not p in exclude:
            objs.append(p)
    
    zipped = [zipfile.is_zipfile(o) and not o.lower().endswith(('.xlsx', '.xls')) \
        for o in objs]
    toappend = []
    todelete = []
    
    for ix, o in enumerate(objs):
        # if zipfile in objs replace zipfile with its contents
        if zipped[ix]:
            for new_o in _path_to_objs(o):
                toappend.append(new_o)
            todelete.append(ix)
    
    shiftindex = 0
    for d in todelete:
        del objs[d - shiftindex]
        shiftindex += 1
    
    for new_o in toappend:
        objs.append(new_o)
    
    return objs

def to_df(obj, cfg={}, raise_on_error=True, silent=False, verbose=False):
    """Convert obj to pandas.DataFrame, determine parser from filename.
    Falls back to odo, esp. for database uri's.
    """
    
    if type(obj) == str:
        name = obj
    else:
        name = obj.name
    name = name[name.rfind('/') + 1:]
    
    if not raise_on_error:
        try:
            return to_df(obj=obj, cfg=cfg, raise_on_error=True)
        except (pd.parser.CParserError, AttributeError, ValueError, TypeError, IOError) as e:
            if not silent:
                print('WARNING in {}: {} {}'.format(name, e.__class__, e))
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

    if verbose:
        print(name, params)
    
    if name.lower().startswith('s3:'):
        if not find_spec('boto'):
        # try:
        #     import boto
        # except:
            raise ImportError('reading from aws-s3 requires the boto package to be installed')
    
    if '.csv' in name.lower():
        # name can be .csv.gz or .csv.bz2
        return pd.read_csv(obj, **params)
        
    elif '.tsv' in name.lower() or '.txt' in name.lower():
        # name can be .tsv.gz or .txt.bz2
        return pd.read_table(obj, **params)
    
    elif name.lower().endswith(('.htm', '.html', '.xml')):
        if not find_spec('lxml'):
        # try:
        #     import lxml
        # except:
            params['flavor'] = 'bs4'
            if not find_spec('bs4') and not find_spec('html5lib'):
            # try:
            #     import bs4
            #     import html5lib
            # except:
                raise ImportError('reading html/xml requires the lxml or bs4 + html5lib packages to be installed')

        if 'nrows' in params:
            del params['nrows']
        
        if type(obj) == zipfile.ZipExtFile:
            obj = obj.read()
        data = pd.read_html(obj, **params)
        data = {str(i): data[i] for i in range(len(data))}
        return data
    
    elif name.lower().endswith('.json'):
        if 'nrows' in params:
            del params['nrows']
        
        return pd.read_json(obj, **params)
    
    elif name.lower().endswith(('.xls', '.xlsx')):
        if not find_spec('xlrd'):
        # try:
        #     import xlrd
        # except:
            raise ImportError('reading excel files requires the xlrd package to be installed')
        
        if 'nrows' in params:
            del params['nrows']
        
        data = {}
        xls = pd.ExcelFile(obj)
        for key in xls.sheet_names:
            data[key] = xls.parse(key, **params)
        return data
    
    elif name.lower().endswith(('.h5', '.hdf5')):
        if not find_spec('tables'):
        # try:
        #     import tables
        # except:
            raise ImportError('reading hdf5 files requires the pytables package to be installed')
        
        if 'nrows' in params:
            del params['nrows']
            # params['chunksize'] = params.pop('nrows') # returns iterator
        
        with pd.HDFStore(obj) as store:
            data = {}
            for key in store.keys():
                data[key[1:]] = store[key]
        return data
    
    elif name.lower().endswith(('.sqlite', '.sql', '.db')):
        import sqlite3
        if type(obj) != str:
            raise IOError('sqlite-database must be decompressed before import')
        
        if 'nrows' in params:
            del params['nrows']
            # params['chunksize'] = params.pop('nrows') # returns iterator
        
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
        try:
            data = {name: odo(obj, pd.DataFrame)}
            if type(data[name]) == pd.DataFrame:
                return data
        except NotImplementedError:
            pass
        raise IOError('Error creating DataFrame from object')

def read(path, cfg={}, filters=[], raise_on_error=False, silent=False, verbose=False, return_errors=False):
    """Wraps pandas.IO & odo to create a dictionary of pandas.DataFrames from multiple different sources
    
    Parameters
    ----------
    path : str
        Location of file, folder or zip-file to be parsed. Can include globbing (`*.csv`).
        Can be remote with URI-notation beginning with e.g. http://, https://, file://, ftp://, s3:// and ssh://.
        Can be odo-supported database (SQL, MongoDB, Hadoop, Spark) if dependencies are available.
        Parser will be selected based on file extension.
    filters : str or list of strings, optional - **will be deprecated**
        For a file to be processed, it must contain one of the Strings (e.g. ['.csv', '.tsv'])
    cfg : dict or str, optional
        Dictionary of kwargs to be provided to the pandas parser (http://pandas.pydata.org/pandas-docs/stable/api.html#input-output)
        or str with path to YAML, that will be parsed.
        
        Special keys:
        
        **filters** : set filters-parameter from config **will be replaced by include, exclude lists**
        
        **default** : kwargs to be used for every file
        
        **custom_date_parser** : strptime-format string (https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior), generates a parser that used as the *date_parser* argument
        
        If filename in keys, use kwargs from that key in addition to or overwriting *default* kwargs.
    silent : boolean, optional
        If True, doesn't print to stdout.
    verbose : boolean, optional
        If True, prints parsing arguments for each file processed to stdout.
    raise_on_error : boolean, optional
        Raise exception or only display warning, if a file cannot be parsed successfully.
    return_errors : boolean, optional
        If True, read() returns (data, errors) tuple instead of only data, with errors as a list of all files that could not be parsed.
        
    Returns
    -------
    data : dict
        Dictionary of parsed pandas.DataFrames, with file names as keys.
    
    Notes
    -----
    - Start with basic cfg and tune until the desired parsing result is achieved.
    - File extensions are critical to determine the parser, make sure they are *common*.
    - Avoid files named 'default' or 'filters'.
    - Avoid duplicate file names.
    - Subfolders and file names beginning with '.' or '_' are ignored.
    - If an https:// URI isn't correctly processed, try http:// instead.
    - To connect to a database or s3-bucket, make sure the required dependencies like sqlalchemy, pymongo, pyspark or boto are available in the active environment.
    """
    
    if type(filters) == str:
        filters = [filters]
    if type(cfg) == str:
        if cfg[0] == '~':
            cfg = os.path.expanduser(cfg)
        yml = _read_yaml(cfg)
        if yml == None:
            if not silent:
                print('creating read.yml config file draft ...')
            cfg = {'filters': ['.csv'], 'default': {'sep': ',', 'parse_dates': []}}
            with open('local/read.yml', 'xt') as f:
                yaml.dump(cfg, f)
            yml = _read_yaml('local/read.yml')
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
    
    for f in _path_to_objs(path):
        if type(f) == str:
            fname = os.path.basename(f)
        elif type(f) == zipfile.ZipExtFile:
            fname = f.name
        else:
            raise RuntimeError('_path_to_objs() returned unknown type', f)
        
        data, errors = _read_append(data=data, errors=errors, path=f, fname=fname, \
            cfg=cfg, raise_on_error=raise_on_error, silent=silent, verbose=verbose)
        
    if raise_on_error and data == {}:
        raise IOError('path is invalid or empty')
    
    if not silent:
        print('imported {} DataFrames'.format(len(data)))
        if len(data) > 0:
            print('total memory usage: {}'.format(mem(data)))
        if len(errors) > 0:
            print('import errors in files: {}'.format(', '.join(errors)))

    if return_errors:
        return data, errors
    else:
        return data

def _read_append(data, errors, path, fname, cfg, raise_on_error, silent, verbose):
    key = fname[fname.rfind('/') + 1:]
    result = to_df(obj=path, cfg=cfg, raise_on_error=raise_on_error, silent=silent, verbose=verbose)
    if type(result) == dict:
        if len(result) == 0:
            errors.append(key)
        # elif len(result) == 1:
        #     r = next(iter(result))
        #     data[r] = result[r]
        else:
            for r in result:
                data['_'.join([key, r])] = result[r]
    elif type(result) == type(None):
        errors.append(key)
    else:
        data[key] = result
    return data, errors

def preview(path, cfg={}, rows=5, silent=True, verbose=False, raise_on_error=False):
    filters = []
    if type(cfg) == str:
        if cfg[0] == '~':
            cfg = os.path.expanduser(cfg)
        yml = _read_yaml(cfg)
        if yml == None:
            yml = {}
        if 'filters' in yml:
            filters = yml['filters']
            if type(filters) == str:
                filters = [filters]
            del yml['filters']
        cfg = yml
        
    if type(cfg) != dict:
        cfg = {'default': {'nrows': rows}}
    else:
        if 'filters' in cfg:
            filters = cfg['filters']
            if type(filters) == str:
                filters = [filters]
            del cfg['filters']
        if 'default' in cfg:
            if type(cfg['default']) == dict:
                cfg['default']['nrows'] = rows
            else:
                cfg['default'] = {'nrows': rows}
        else:
            cfg['default'] = {'nrows': rows}

    if silent:
        # if not silent, output will be generated from icy.read()
        print('processing', path, '...')
    
    prev, errors = read(path=path, cfg=cfg, silent=silent, verbose=verbose, \
        raise_on_error=raise_on_error, return_errors=True)

    for key in sorted(prev):
        print('File: {}'.format(key))
        print()
        prev[key].info(verbose=True, memory_usage=True, null_counts=True)
        print()
        print('{:<20} | first {} VALUES'.format('COLUMN', rows))
        print('-'*40)
        for col in prev[key].columns:
            print('{:<20} | {}'.format(col, str(list(prev[key][col].values)[:rows])))
        print('='*40)

    print('Successfully parsed first {} rows of {} files:'.format(rows, len(prev)))
    print(', '.join(sorted(prev)))
    
    if len(errors) > 0 and silent:
        print('Errors parsing files: {}'.format(', '.join(errors)))
        print()
        print('Try icy.preview(path, cfg, silent=False) for a more verbose output.')
    return
    
def mem(data):
    """Total memory used by data
    
    Parameters
    ----------
    data : dict of pandas.DataFrames or pandas.DataFrame
    
    Returns
    -------
    str : str
        Human readable amount of memory used with unit (like KB, MB, GB etc.).
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

def _read_yaml(path):
    if os.path.isfile(path):
        with open(path) as f:
            return yaml.safe_load(f)
    else:
        return None
    
def merge(data, cfg=None):
    """ WORK IN PROGRESS
    
    Concat, merge, join, drop keys in dictionary of pandas.DataFrames
    into one pandas.DataFrame (data) and a pandas.Series (labels).
    
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
        cfg = _read_yaml(cfg)
    if cfg == None:
        cfg = _read_yaml('local/merge.yml')
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
            with open('local/merge.yml', 'xt') as f:
                yaml.dump(cfg, f)
            cfg = _read_yaml('local/merge.yml')
    
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

def _find_key_cols(df):
    """Identify columns in a DataFrame that could be a unique key"""
    
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

def run_examples(examples):
    """Run read() on a number of examples, supress output, generate summary.
    
    Parameters
    ----------
    examples : list of tuples of three str elements
        Tuples contain the path and cfg argument to the read function,
        as well as the cfg argument to the merge function (*TODO*)
        e.g. [(path, read_cfg, merge_cfg), (...)]
    
    Returns
    -------
    None
        Prints all results to stdout.
    """
    
    import inspect

    PATH_TEST_DATA = os.path.join(os.path.dirname(os.path.abspath( \
        inspect.getfile(inspect.currentframe()))), '../local/test_data')
    
    print('running examples ...')
    t0 = datetime.now()
    results = [0, 0, 0]
    for ex in sorted(examples):
        t1 = datetime.now()
        src, cfg, _ = examples[ex]
        src = os.path.abspath(os.path.join(PATH_TEST_DATA, src))
        if not os.path.isfile(src) and not os.path.isdir(src):
            print('{} not a file'.format(src))
            break
        if type(cfg) == str:
            cfg = os.path.abspath(os.path.join(PATH_TEST_DATA, cfg))
            if not os.path.isfile(cfg):
                print('{} not a file'.format(cfg))
                break
        try:
            data = read(src, cfg=cfg, silent=True)
            n_keys = len(data.keys())
            if n_keys > 0:
                print('data {:<15} [SUCCESS]   {:.1f}s, {} dfs, {}'.format(
                    ex, (datetime.now()-t1).total_seconds(), n_keys, mem(data)))
                results[0] += 1
            else:
                print('data {:<15} [NO IMPORT] {:.1f}s'.format(ex, (datetime.now()-t1).total_seconds()))
                results[1] += 1
        except:
            print('data {:<15} [EXCEPTION] {:.1f}s'.format(ex, (datetime.now()-t1).total_seconds()))
            results[2] += 1
    print()
    print('ran {} tests in {:.1f} seconds'.format(len(examples),
        (datetime.now()-t0).total_seconds()))
    print('{} success / {} no import / {} exception'.format(
        str(results[0]), str(results[1]), str(results[2])))

if __name__ == '__main__':
    run_examples(examples)
    