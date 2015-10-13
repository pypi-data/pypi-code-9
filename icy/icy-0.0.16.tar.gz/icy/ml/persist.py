import pandas as pd
import os
import sys
from tables.scripts import ptrepack
from copy import deepcopy

def store_data_h5(data, filename):
    print('writing data ... \t', end='')
    with pd.HDFStore(filename, complevel=9, complib='blosc') as store:
        for k in data:
            store[k] = data[k]
    print('[OK]')
    return
    
def load_data_h5(filename):
    print('loading data ... \t', end='')
    data = {}
    with pd.HDFStore(filename, complevel=9, complib='blosc') as store:
        for k in store.keys():
            data[k.replace('/', '')] = store[k]
    print('[OK]')
    return data
    
def repack_h5(filename):
    print('repacking store ... \t', end='')
    backup = deepcopy(sys.argv)
    sys.argv = 'ptrepack --chunkshape=auto --propindexes --complevel=9 --complib=blosc {} {}'.format(filename, 'tmp.h5').split(' ')
    ptrepack.main()
    os.remove(filename)
    os.rename(tmp, filename)
    sys.argv = backup
    print('[OK]')
    return
