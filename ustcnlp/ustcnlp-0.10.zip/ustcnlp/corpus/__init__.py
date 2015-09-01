# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
'''
 * __init__.py source file
 *
 * Copyright (c) 2014-2015 USTC-CMET
 * This file is part of the Automatic Essay Scoring Engine.
 * Significant contributions : Cheng Ding, WeiWei Duan
 *
 * History:
 * --------
 * 2015/05/31 - created (Cheng Ding)
'''

from .. import utils

_path = utils.PathObj(utils.path_join(utils.extract_dir(__file__), '../../../../../data/corpus'))
