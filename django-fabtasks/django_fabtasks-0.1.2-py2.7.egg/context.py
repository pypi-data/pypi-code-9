# -*- coding: utf-8 -*-

# Copyright 2015
#
# This file is part of proprietary software and use of this file
# is strictly prohibited without written consent.
#
# @author  Tim Santor  <tsantor@xstudios.agency>

# -----------------------------------------------------------------------------

# 3rd Party
from fabric.api import *
from contextlib import contextmanager

# -----------------------------------------------------------------------------


@contextmanager
def virtualenv():
    with cd(env.project_root):
        with prefix('source ' + env.activate):
            yield
