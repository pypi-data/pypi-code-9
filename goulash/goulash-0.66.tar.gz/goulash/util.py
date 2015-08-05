""" goulash.util
"""
import time
import uuid

from goulash._os import home, summarize_fpath  # backwards compat.


def uniq(use_time=False):
    """ """
    result = str(uuid.uuid1())
    if use_time:
        result += str(time.time())[:-3]
    return result
