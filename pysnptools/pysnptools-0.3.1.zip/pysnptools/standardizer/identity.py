import numpy as np
import scipy as sp
import logging
from pysnptools.standardizer import Standardizer

class Identity(Standardizer):
    '''
    A :class:`.Standardizer` that does nothing to SNP data.

    See :class:`.Standardizer` for more information about standardization.

    >>> from pysnptools.standardizer import Identity
    >>> from pysnptools.snpreader import Bed
    >>> snpdata1 = Bed('../../tests/datasets/all_chr.maf0.001.N300').read()
    >>> print snpdata1.val[0,0]
    2.0
    >>> snpdata1 = snpdata1.standardize(Identity())
    >>> print snpdata1.val[0,0]
    2.0
    '''

    def __init__(self):
        pass

    def standardize(self, snps, block_size=None, force_python_only=False):
        if block_size is not None:
            warnings.warn("block_size is deprecated (and not needed, since standardization is in-place", DeprecationWarning)
        return snps

    #changes snpdata.val in place
    def _train_standardizer(self,snpdata,apply_in_place,force_python_only=False):
        return self


    def __repr__(self): 
        return "{0}()".format(self.__class__.__name__)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    import doctest
    doctest.testmod()
