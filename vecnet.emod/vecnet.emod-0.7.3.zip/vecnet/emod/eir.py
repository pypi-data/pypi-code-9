#!/usr/bin/python
#
# This file is part of the vecnet.emod package.
# For copyright and licensing information about this package, see the
# NOTICE.txt and LICENSE.txt files in its top-level directory; they are
# available at https://github.com/vecnet/vecnet.emod
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License (MPL), version 2.0.  If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

import math


def prevalence(eir):
    """
EIR to prevalence conversion. This relationship is used by Philip Eckhoff to calibrate EMOD model.

Please refer to paper below for additional details
Smith, D. L., Dushoff, J., Snow, R. W., & Hay, S. I. (2005). The entomological inoculation rate and Plasmodium
falciparum infection in African children. Nature, 438(7067) 492-495.doi:10.1038/nature04024
http://www.ncbi.nlm.nih.gov/pmc/articles/PMC3128496/#FD1
"""
    pf = 1 - math.pow(1 + 0.45*4.2*eir, -0.238)
    return pf
