"""
Seemingly Unrelated Regression

Author: Chad Fulton
License: Simplified-BSD
"""

import numpy as np
import pandas as pd
from ..model import Model

class SUR(Model):
    def __init__(self, endog, *args, **kwargs):
        # Setup (empty) dimensions
        self.nobs = None
        self.k_endog = None

        # Initialize the model
        super(SUR, self).__init__(endog, *args, **kwargs)
