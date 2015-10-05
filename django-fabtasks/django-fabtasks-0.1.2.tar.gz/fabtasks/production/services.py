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
#from fabric.contrib import project
#from fabric.contrib.console import confirm

#from fabtasks.context import virtualenv

# -----------------------------------------------------------------------------


@task
def apache_restart():
    """Restart apache"""
    run(env.apache_restart_command)
