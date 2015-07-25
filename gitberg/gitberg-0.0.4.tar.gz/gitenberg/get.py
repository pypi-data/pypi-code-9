#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Gets an existing GITenberg repo and makes a local clone
"""

from __future__ import print_function
import os

import sh


class GitBookGetter():
    """
    """

    def __init__(self, book):
        self.book = book

