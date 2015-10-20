# -*- coding: utf-8 -*-
from path import path


class MIP(object):

    """Wrapper for control class for MIP pipeline.

    Args:
        base_path (path): path to root of MIP setup
    """

    def __init__(self, base_path):
        super(MIP, self).__init__()
        self.base_path = path(base_path)
