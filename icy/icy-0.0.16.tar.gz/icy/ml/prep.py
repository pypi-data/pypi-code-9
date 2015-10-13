import pandas as pd
import numpy as np
import scipy.sparse as sparse
from xgboost import DMatrix
from copy import deepcopy
from sklearn.preprocessing import StandardScaler, MinMaxScaler

def drop_nan_bulk(data, how='all', axes=[0, 1]):
    for key in data:
        for axis in axes:
            # axis=0: rows, axis=1: cols
            # how=all: drop if all values are nan, how=any: drop if any value is nan
            data[key].dropna(axis=axis, how=how, inplace=True)
    return data

def fill_nan_bulk(data, fill='const'):
    if fill in ['mean', 'median', 'mode', 'min', 'max']:
        for key in data:
            data[key].fillna(-1, inplace=True)
            for col in data[key].select_dtypes(include=[np.number]):
                if fill == 'mean':
                    data[key].loc[:, col].replace(-1, data[key].loc[:, col].mean(), inplace=True)
                elif fill == 'median':
                    data[key].loc[:, col].replace(-1, data[key].loc[:, col].median(), inplace=True)
                elif fill == 'mode':
                    data[key].loc[:, col].replace(-1, data[key].loc[:, col].mode(), inplace=True)
                elif fill == 'min':
                    data[key].loc[:, col].replace(-1, data[key].loc[:, col].min(), inplace=True)
                elif fill == 'max':
                    data[key].loc[:, col].replace(-1, data[key].loc[:, col].max(), inplace=True)
    elif fill == 'const':
        for key in data:
            data[key].fillna(-1, inplace=True)
    elif type(fill) == [int, str]:
        for key in data:
            data[key].fillna(fill, inplace=True)
    return data

def scale_minmax_bulk(scale, data):
    for key in data:
        data[key] = pd.DataFrame(MinMaxScaler(scale).fit_transform(data[key]), index=data[key].index, columns=data[key].columns)
    return data

def scale_std_bulk(data, mean=True, std=True):
    for key in data:
        data[key] = pd.DataFrame(StandardScaler(with_mean=mean, with_std=std).fit_transform(data[key]), index=data[key].index, columns=data[key].columns)
    return data
    
def remove_duplicates_bulk(data):
    for key in data:
        print(key, 'rows')
        data[key] = data[key].drop_duplicates() # rows
        print(key, 'cols')
        data[key] = data[key].T.drop_duplicates().T # columns - very slow, try ndarray.swapaxes() ?
    return data

def convert_numeric_bulk(data, dtype=None, strict=False):
    for k in data:
        if dtype != None:
            if strict:
                data[k] = data[k].astype(dtype)
            else:
                for col in data[key].select_dtypes(exclude=[np.number]):
                    data[k].loc[:, col] = data[k].loc[:, col].astype(dtype)
                # for col in data[k]:
                #     if data[k][col].dtype not in ['bool', 'int64', 'float64']:
                #         data[k].loc[:, col] = data[k].loc[:, col].astype(dtype)
        else:
            data[k] = data[k].convert_objects(convert_dates=False, convert_numeric=True, convert_timedeltas=False)
    return data

def to_dmatrix(data, labels=None):
    if type(data) in [pd.DataFrame, pd.Series]:
        if labels != None and type(labels) in [pd.DataFrame, pd.Series]:
            return DMatrix(data.values, labels.values)
        else:
            return DMatrix(data.values)
    else:
        if labels != None:
            return DMatrix(data, labels)
        else:
            return DMatrix(data)

def to_sparse(data, kind='csr', fill_value=0):
    # add csc, coo variants?
    if type(data) in [pd.DataFrame, pd.Series]:
        data = data.to_sparse(fill_value)
    elif type(data) == np.ndarray:
        data = sparse.csr_matrix(data)
    return data

def to_dense(data):
    # add csc, coo variants?
    if type(data) in [pd.DataFrame, pd.Series]:
        data = data.to_dense()
    else:
        data = pd.DataFrame(data.todense())
    return data

def join(data, joins):
    for key1, key2, col in joins:
        if type(col) == str:
            if col in data[key1] or col in data[key2]:
                proceed = True
            else:
                proceed = False
        else:
            for e in col:
                if e in data[key1] or e in data[key2]:
                    proceed = True
                else:
                    proceed = False
                    break
        if proceed:
            data[key2].columns = [key2+'_'+c for c in data[key2].columns]
            try:
                if type(col) == str:
                    right_on = key2 + '_' + col
                else:
                    right_on = [key2 + '_' + c for c in col]
                data[key1] = pd.merge(data[key1], data[key2], how='left', left_on=col, right_on=right_on, sort=False)
            except KeyError:
                data[key1] = data[key1].join(data[key2], on=col)

    for key1, key2, col in joins:
        # if col in data[key1]:
        #     data[key1].drop(col, axis=1, inplace=True)
        if key2 in data:
            del data[key2]
    return data
