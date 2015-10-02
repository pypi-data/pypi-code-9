import sys

sys.path.append('apps/severe_slug')
from severe_slug import my_fun

from multiprocessing import Pool
import numpy as np


def test(val):
    print val
    inputs = {'InflowL': '0.4', 'H1': '1', 'H2': '0.5', 'H3': '0.5', 'InflowG': str(val), 'a1': '0', 'a2': '30',
              'Radius': '0.05', 'Name': 'test_loop'}
    my_fun(inputs)


inflowgs = [0.01, 0.02, 0.03]
print inflowgs
pool = Pool(3)
results = pool.map(test, inflowgs)


