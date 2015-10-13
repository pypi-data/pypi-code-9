import numpy as np

def show_dtypes(data):
    for key in data:
        print(key)
        print(data[key].get_dtype_counts())
        print()

def show_cat_uniques(data):
    for key in data:
        print(key, data[key].shape)
        for col in data[key].select_dtypes(exclude=[np.number]):
            print(col, len(data[key][col].unique()))
        print()

def show_nan(data):
    for key in data:
        print(key, data[key].shape)
        for col in data[key]:
            nans = sum(data[key][col].isnull())
            if nans > 0:
                print(col, nans)
        print()

def show_cov(data, labels, top=3):
    top_cov = []
    for col in data.select_dtypes(include=[np.number]):
        cov = labels.cov(data[col])
        if len(top_cov) < top or cov > min([e[1] for e in top_cov]):
            if not np.isnan(cov):
                top_cov.append((col, cov))
                top_cov = sorted(top_cov, key=lambda x: x[1], reverse=True)[:top]
    if len(top_cov) > 0:
        for e in top_cov:
            print(e[0], e[1])
        print()

def show_corr(data, labels, top=3, high=True):
    top_corr = []
    for col in data.select_dtypes(include=[np.number]):
        corr = labels.corr(data[col])
        if high:
            if len(top_corr) < top or corr > min([e[1] for e in top_corr]):
                if not np.isnan(corr):
                    top_corr.append((col, corr))
                    top_corr = sorted(top_corr, key=lambda x: x[1], reverse=True)[:top]
        else:
            if len(top_corr) < top or corr < max([e[1] for e in top_corr]):
                if not np.isnan(corr):
                    top_corr.append((col, corr))
                    top_corr = sorted(top_corr, key=lambda x: x[1], reverse=False)[:top]
            
    if len(top_corr) > 0:
        for e in top_corr:
            print(e[0], e[1])
        print()