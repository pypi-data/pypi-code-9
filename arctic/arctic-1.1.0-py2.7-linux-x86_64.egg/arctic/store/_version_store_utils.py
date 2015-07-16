from bson import Binary
import hashlib
import numpy as np
import pickle
import pandas as pd
import functools
from pandas.compat import pickle_compat

def _split_arrs(array_2d, slices):
    """
    Equivalent to numpy.split(array_2d, slices),
    but avoids fancy indexing
    """
    if len(array_2d) == 0:
        return np.empty(0, dtype=np.object)

    rtn = np.empty(len(slices) + 1, dtype=np.object)
    start = 0
    for i, s in enumerate(slices):
        rtn[i] = array_2d[start:s]
        start = s
    rtn[-1] = array_2d[start:]
    return rtn


def checksum(symbol, doc):
    """
    Checksum the passed in dictionary
    """
    sha = hashlib.sha1()
    sha.update(symbol)
    for k in sorted(doc.iterkeys(), reverse=True):
        sha.update(str(doc[k]))
    return Binary(sha.digest())


def cleanup(arctic_lib, symbol, version_ids):
    """
    Helper method for cleaning up chunks from a version store
    """
    collection = arctic_lib.get_top_level_collection()

    # Remove any chunks which contain just the parents, at the outset
    # We do this here, because $pullALL will make an empty array: []
    # and the index which contains the parents field will fail the unique constraint.
    for v in version_ids:
        # Remove all documents which only contain the parent
        collection.delete_many({'symbol': symbol,
                               'parent': {'$all': [v],
                                          '$size': 1},
                               })
        # Pull the parent from the parents field
        collection.update_many({'symbol': symbol,
                                'parent': v},
                               {'$pull': {'parent': v}})

    # Now remove all chunks which aren't parented - this is unlikely, as they will
    # have been removed by the above
    collection.delete_one({'symbol':  symbol, 'parent': {'$size': 0}})


def _define_compat_pickle_load():
    """Factory function to initialise the correct Pickle load function based on
    the Pandas version.
    """
    if pd.version.version.startswith("0.14"):
        return pickle.load
    return functools.partial(pickle_compat.load, compat=True)

# Initialise the pickle load function and delete the factory function.
pickle_compat_load = _define_compat_pickle_load()
del _define_compat_pickle_load
