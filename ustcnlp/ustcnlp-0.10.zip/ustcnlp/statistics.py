# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
import math
from . import utils

def __attrs(es_lst, key):
    return map(lambda d:float(d.__getattribute__(key)), es_lst)

def __is_str(s):
    try:
        s = s + '!'
    except:
        s = ''
    return s and True or False

def count(items, dup_free=False):
    '''
    返回列表中元素个数，dup_free为True时，不计重复元素
    '''
    return len(set(items)) if dup_free else len(items)

def mean(items, dvalue=0):
    '''
    计算平均值，若没有任何元素则返回默认值
    '''
    d, c = 0, 0
    for x in items:
        d += x
        c += 1
    return d / c if c else dvalue

def t_test(es_lst_a, es_lst_b, key_or_keys):
    from scipy import stats
    #t检验，es_lst_a、es_lst_b为两组作文, key_or_keys为键或键列表
    if __is_str(key_or_keys):
        return stats.ttest_ind(__attrs(es_lst_a, key_or_keys), __attrs(es_lst_b, key_or_keys))
    else:
        return map(lambda s: stats.ttest_ind(__attrs(es_lst_a, s), __attrs(es_lst_b, s)), key_or_keys)

def pearsonr(es_lst, key, key_or_keys):
    from scipy import stats
    #pearson相关系数，es_lst为作文列表，返回pearson(key, key ∈ key_or_keys)
    lst = __attrs(es_lst, key)
    if __is_str(key_or_keys):
        return stats.pearsonr(lst, __attrs(es_lst, key_or_keys))
    else:
        return map(lambda s: stats.pearsonr(lst, __attrs(es_lst, s)), key_or_keys)

def __simpls(X, Y, factors= -1):
    '''
    使用simpls算法进行偏最小二乘法分析
    参考文献: http://www.statsoft.com/textbook/partial-least-squares/
    For each h=1,...,c, where A0=X'Y, M0=X'X, C0=I, and c given,
       1. compute qh, the dominant eigenvector of Ah'Ah
       2. wh=Ahqh, ch=wh'Mhwh, wh=wh/sqrt(ch), and store wh into W as a column
       3. ph=Mhwh, and store ph into P as a column
       4. qh=Ah'wh, and store qh into Q as a column
       5. vh=Chph, and vh=vh/||vh||
       6. Ch+1=Ch - vhvh' and Mh+1=Mh - phph'
       7. Ah+1=ChAh
    '''
    from scipy import linalg
    import numpy as np
    X = np.asmatrix(X)
    Y = np.asmatrix(Y)
    if factors < 0 or factors > min(X.shape[0] - 1, X.shape[1]):
        factors = min(X.shape[0] - 1, X.shape[1])
    if Y.shape[0] != X.shape[0]:
        Y = Y.reshape(Y.shape[1], Y.shape[0])
    #标准化
    X_Mean = np.mean(X, 0)
    Y_Mean = np.mean(Y, 0)
    X_Std = np.std(X, 0)
    Y_Std = np.std(Y, 0)
    for i in range(X_Std.shape[1]):
        if X_Std[0, i] < 1.0e-20:
            X_Std[0, i] = 1
    for i in range(Y_Std.shape[1]):
        if Y_Std[0, i] < 1.0e-20:
            Y_Std[0, i] = 1
    X = (X - X_Mean) / X_Std
    Y = (Y - Y_Mean) / Y_Std
    #使用simpls算法计算B
    W, P, Q = list(), list(), list()
    A = X.T * Y
    M = X.T * X
    C = np.asmatrix(np.diag([1] * X.shape[1]))
    iteration = 0
    while iteration < factors:
        iteration += 1
        q = linalg.svd(A, False)[2][:, 0:1]
        w = A * q
        ch = w.T * M * w
        if ch < 1.0e-20:
            break
        w = w / math.sqrt(ch)
        W.append(w.A.reshape(len(w)))
        p = M * w
        P.append(p.A.reshape(len(p)))
        q = A.T * w
        Q.append(q.A.reshape(len(q)))
        v = C * p
        v = v / linalg.norm(v)
        C = C - v * v.T
        M = M - p * p.T
        A = C * A
    W = np.asmatrix(W).T
    P = np.asmatrix(P).T
    Q = np.asmatrix(Q).T
    B = W * Q.T
    #逆标准化和技术E值
    B = (B.T / X_Std).T / (1 / Y_Std)
    E = -X_Mean * B + Y_Mean
    return B, E

class __PLS(object):
    def __init__(self, BE, XKeys, YKeys):
        self.B = BE[0]
        self.E = BE[1]
        self.XKeys = list(XKeys)
        self.YKeys = list(YKeys)
    def predict(self, es_lst, tail=''):
        v = [[es.__getattribute__(key) for key in self.XKeys] for es in es_lst]
        v = (v * self.B + self.E).A
        for index1, es in enumerate(es_lst):
            for index2, key in enumerate(self.YKeys):
                es.__setattr__(key + tail, v[index1][index2])
        return [es.__getattribute__(key + tail) for es in es_lst]

def pls_regression(es_lst, XKeys, YKeys, factors= -1):
    #使用simpls算法进行回归分析，返回PLS类
    X, Y = [[[es.__getattribute__(key) for key in keys] for es in es_lst] for keys in [XKeys, YKeys]]
    return __PLS(__simpls(X, Y, factors), XKeys, YKeys)

if __name__ == '__main__':
    X = [[7, 7, 13, 7],
        [4, 3, 14, 7],
        [10, 5, 12, 5],
        [16, 7, 11, 3],
        [13, 3, 10, 3], ]
    Y = [[14, 7, 8],
          [10, 7, 6],
          [8, 5, 5],
          [2, 4, 7],
          [6, 2, 4],
          ]
    B, E = __simpls(X, Y, 4)
    Z = X * B + E
    print(X * B + E)
    #
    O = [utils.BaseClass(x1=X[i][0], x2=X[i][1], x3=X[i][2], x4=X[i][3], y1=Y[i][0], y2=Y[i][1], y3=Y[i][2]) for i in xrange(len(X))]
    pls = pls_regression(O, ['x1', 'x2', 'x3', 'x4'], ['y1', 'y2', 'y3'])
    pls.predict(O, '_pd')
    print([[es.y1_pd, es.y2_pd, es.y3_pd] for es in O])

