#!/usr/bin/env python3
"""
Sub-Package COMM.CLASSES of Package PLIB3 -- Python Class Objects
Copyright (C) 2008-2015 by Peter A. Donis

Released under the GNU General Public License, Version 2
See the LICENSE and README files for more information
"""

from plib.stdlib.util import ModuleProxy

ModuleProxy(__name__).init_proxy(__name__, __path__, globals(), locals())

# Now clean up our namespace
del ModuleProxy
