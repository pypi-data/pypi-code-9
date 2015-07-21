# Copyright(c) 2014, The scLVM developers (Forian Buettner, Paolo Francesco Casale, Oliver Stegle)
#
#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.

__all__ = ['']

__version__ = '0.1'

def versiontuple(v):
    return tuple(map(int, (v.split("."))))

import limix
try:
    limix.__version__
    if versiontuple(limix.__version__)>versiontuple('0.7.3'):
        import limix.deprecated as limix
        import limix.deprecated.modules.panama as PANAMA
        import limix.deprecated.modules.varianceDecomposition as VAR
        import limix.deprecated.modules.qtl as QTL
    else:
        import limix.modules.panama as PANAMA
        import limix.modules.varianceDecomposition as VAR
        import limix.modules.qtl as QTL	
except:
    import limix.deprecated as limix    
    import limix.deprecated.modules.panama as PANAMA
    import limix.deprecated.modules.varianceDecomposition as VAR
    import limix.deprecated.modules.qtl as QTL	
    
import core
from core import *
from core import scLVM
import gp_clvm
from gp_clvm import gpCLVM


def getVerbose(verbose):
	"""resolve verbose flag, using module settings if verbose=None"""
	if verbose is None:
		verbose = limix.verbose
	else:
		verbose = verbose
	return verbose
