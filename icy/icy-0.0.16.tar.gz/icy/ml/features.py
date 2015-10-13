import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import HashingVectorizer, TfidfVectorizer

def extract_dates(data, features, replace=True):
    print('date features ... \t', end='')
    
    for k in data:
        for col in data[k]:
            if 'datetime64' in data[k][col].dtype.name:
                if 'year' in features:
                    data[k].loc[:, col+'_year'] = data[k][col].dt.year
                if 'month' in features:
                    data[k].loc[:, col+'_month'] = data[k][col].dt.month
                if 'day' in features:
                    data[k].loc[:, col+'_day'] = data[k][col].dt.day
                if 'week' in features:
                    data[k].loc[:, col+'_week'] = data[k][col].dt.week
                if 'quarter' in features:
                    data[k].loc[:, col+'_quarter'] = data[k][col].dt.quarter
                if 'weekday' in features:
                    data[k].loc[:, col+'_weekday'] = data[k][col].dt.weekday
                if 'hour' in features:
                    data[k].loc[:, col+'_hour'] = data[k][col].dt.hour
                if 'minute' in features:
                    data[k].loc[:, col+'_minute'] = data[k][col].dt.minute
                
                if replace:
                    data[k].drop(col, axis=1, inplace=True)
    
    print('[OK]')
    return data

def encode_cols(encoder, data, keys):
    cols = []
    for fn in data:
        for key in keys:
            if key in data[fn].columns:
                cols.append((fn, data[fn].loc[data[fn][key].notnull(), key]))
    values = pd.concat([c[1] for c in cols], axis=0, ignore_index=True)
    enc = encoder.fit(values)
    if type(encoder) == LabelEncoder:
        for fn, c in cols:
            data[fn].loc[data[fn][c.name].notnull(), c.name] = enc.transform(c.loc[c.notnull()])
    elif type(encoder) == HashingVectorizer:
        for fn, c in cols:
            new_cols = pd.DataFrame(enc.transform(data[fn].loc[:, c.name].astype(str)).toarray()).astype('bool')
            new_cols.columns = new_cols.columns.astype(str)
            while any(data[fn].columns.isin(new_cols.columns)):
                new_cols.columns = [str(n)+'_1' for n in new_cols.columns]
            data[fn] = pd.concat([data[fn], new_cols], axis=1)
            data[fn].drop(c.name, axis=1, inplace=True)
    elif type(encoder) == TfidfVectorizer:
        for fn, c in cols:
            new_cols = pd.DataFrame(enc.transform(data[fn].loc[:, c.name].astype(str)).toarray())
            new_cols.columns = new_cols.columns.astype(str)
            while any(data[fn].columns.isin(new_cols.columns)):
                new_cols.columns = [str(n)+'_1' for n in new_cols.columns]
            data[fn] = pd.concat([data[fn], new_cols], axis=1)
            data[fn].drop(c.name, axis=1, inplace=True)
    return data

def encode(kind, data, keys, hashing_n_features=None):
    print('encoding features ... \t', end='')

    if kind == 'label':
        for k in keys:
            encode_cols(LabelEncoder(), data, k)
    elif kind == 'hashing':
        for k in keys:
            encode_cols(HashingVectorizer(n_features=hashing_n_features), data, k)
    elif kind == 'tfidf':
        for k in keys:
            encode_cols(TfidfVectorizer(), data, k)
    else:
        print('unknown encoder', kind)

    print('[OK]')
    return data

def leave_one_out_encoding(c_train, c_test, y):
    encoded_train = c_train.copy()
    encoded_test = c_test.copy()
    unique_categories = np.array(list(set(c_train).union(set(c_test))))
    # print(unique_categories)
    for c in unique_categories:
        c_counts = np.sum(c_train == c)
        if c_counts == 0:
            encoded_test[c_test == c] = 0.5
        elif c_counts == 1:
            encoded_train[c_train == c] = 0.5
            encoded_test[c_test == c] = 0.5
        else:
            positive_c = np.logical_and(c_train == c, y == 1)
            negative_c = np.logical_and(c_train == c, y == 0)
            positive_c_count = np.sum(positive_c)
            negative_c_count = np.sum(negative_c)
            
            encoded_train[positive_c] = 1.0 * (positive_c_count - 1) / (c_counts - 1)
            encoded_train[negative_c] = 1.0 * (positive_c_count) / (c_counts - 1)
            encoded_test[c_test == c] = 1.0 * (positive_c_count) / (c_counts)
            
    noise = np.random.normal(1.0, 0.1, len(c_train))
    encoded_train = encoded_train * noise
    
    return encoded_train, encoded_test
