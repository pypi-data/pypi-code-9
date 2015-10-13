#!/usr/bin/env python
# -*- coding: utf-8 -*-


from .sqldf import SQLDF
from .load import load_iris, load_meat, load_births

__version__ = "1.2.2"
__all__ = [
    "SQLDF",
    "load_iris",
    "load_meat",
    "load_births"
]
