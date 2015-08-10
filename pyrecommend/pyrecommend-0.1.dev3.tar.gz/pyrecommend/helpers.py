# coding: utf-8
"""Utilities that make experimenting in a Python shell easier."""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)


def make_data(score_list):
    """Make numbered data dictionaries from a list of lists.

    This is for easily simulating scores for items by ID, rated by users where
    the users are identified by ID as well.

    This is to help when playing in the shell.

    >>> make_data([[5, 20], [30, 9]]) == {1: {1: 5, 2: 20}, 2: {1: 30, 2: 9}}
    True

    """
    data = {i+1: {j+1: v for j, v in enumerate(scores) if v != 0}
            for i, scores in enumerate(score_list)}
    return data
