import os
import zipfile
import pandas as pd
from copy import deepcopy

def to_df(obj, cfg={}, error='raise'):
    if type(obj) == str:
        name = obj
    else:
        name = obj.name
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
            data[key.lower()] = xls.parse(key, **params)
        return data
    elif name.endswith('.h5'):
        try:
            import tables
        except:
            raise ImportError('reading hdf5 files requires the pytables package to be installed')
        with pd.HDFStore(obj) as store:
            data = {}
            for key in store:
                data[key[1:].lower()] = store[key]
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
                data[t.lower()] = pd.read_sql_query(sql, con, **params)
        return data
    else:
        if error == 'raise':
            raise AttributeError('object', name, 'not recognized for DataFrame import')
        else:
            return None
    
def read(path, select=None, cfg={}):
    data = {}
    if os.path.isdir(path):
        # path is folder
        print('processing directory')
        if select != None:
            files = [e for e in os.listdir(path) if select in e]
        else:
            files = [e for e in os.listdir(path)]
        for fn in files:
            with open(os.path.join(path, fn)) as file:
                if '/' in fn:
                    key = fn.rsplit('/', 1)[1].lower()
                else:
                    key = fn.lower()
                result = to_df(file, cfg)
                if type(result) == dict:
                    for r in result:
                        data['_'.join([key,r])] = result[r]
                else:
                    data[key] = result
    
    elif os.path.exists(path):
        # path is file
        if path.endswith('.sql') or path.endswith('.sqlite') \
            or path.endswith('.xlsx') or path.endswith('.xls') \
            or path.endswith('.gz') or path.endswith('.bz2'):
            print('processing file')
            # these mustn't be openend before calling to_df()
            if '/' in path:
                key = path.rsplit('/', 1)[1].lower()
            else:
                key = path.lower()
            result = to_df(path, cfg)
            if type(result) == dict:
                for r in result:
                    data['_'.join([key, r])] = result[r]
            else:
                data[key] = result
        else:
            if zipfile.is_zipfile(path):
                # path is zipfile
                # !identifies xlsx as archive of xml files
                print('processing zip-archive')
                with zipfile.ZipFile(path) as myzip:
                    if select != None:
                        files = [e for e in myzip.namelist() if select in e]
                    else:
                        files = [e for e in myzip.namelist()]
                    for fn in files:
                        with myzip.open(fn) as file:
                            if '/' in fn:
                                key = fn.rsplit('/', 1)[1].lower()
                            else:
                                key = fn.lower()
                            result = to_df(file, cfg)
                            if type(result) == dict:
                                for r in result:
                                    data['_'.join([key,r])] = result[r]
                            else:
                                data[key] = result
            else:
                # not a folder
                # not a file that may not be opened before calling to_df()
                # not a zipfile
                print('processing file')
                with open(path) as file:
                    if '/' in path:
                        key = path.rsplit('/', 1)[1].lower()
                    else:
                        key = path.lower()
                    result = to_df(file, cfg)
                    if type(result) == dict:
                        for r in result:
                            data['_'.join([key,r])] = result[r]
                    else:
                        data[key] = result
    else:
        # if type(path) == sqlalchemy.engine:
        #     raise NotImplemented('SQLAlchemy support is not yet available')
        # elif type(path) == pymongo.MongoClient():
        #     raise NotImplemented('pymongo support is not yet available')
        # elif path is elasticsearch Elasticsearch():
        #     raise NotImplemented('elasticsaerch support is not yet available')
                    
        raise AttributeError('path must be valid file, folder or zip-archive')
    
    print('imported {} DataFrames'.format(len(data.keys())))
    return data

def merge(data, cfg=None):
    # get from a dict of dataframes to one dataframe (data) and one series (labels)
    # pd.concat([df1, df2], join, join_axes, ignore_index) and pd.merge(left, right, how, on, suffixes)
    # should be easy to iterate from nothing to a fully joined set of dataframes
    
    # default_cfg = cfg.json, .ini, .cfg, .yaml
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

