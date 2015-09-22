"""
State Space Composite Representation

Author: Chad Fulton
License: Simplified-BSD
"""
from __future__ import division, absolute_import, print_function

from warnings import warn

import numpy as np
from .representation import Representation


class CompositeRepresentation(Representation):
    r"""
    Composite representation from linearly combining several independent
    state space representations
    """
    def __init__(self, *args, **kwargs):
        self.representations = []
        self.endog = []

        # Get the list of Representations, eliminating any existing
        # composite representations
        for arg in args:
            if isinstance(arg, CompositeRepresentation):
                self.representations += arg.representations
            elif isinstance(arg, Representation):
                self.representations.append(arg)
            else:
                raise ValueError('Invalid statespace representation provided')

        # Get the list of endogenous variables
        k_states = np.sum([mod.k_states for mod in self.representations])


        # Calculate state-space indices which will be used to combine the
        # child representations' matrices