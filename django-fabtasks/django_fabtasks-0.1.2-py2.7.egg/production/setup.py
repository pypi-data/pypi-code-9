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

from fabtasks.context import virtualenv

# -----------------------------------------------------------------------------


@task
def pip_install_requirements():
    """Install pip requirements from requirements.txt"""
    with virtualenv():
        run('pip install -r requirements.txt')


@task
def pip_update():
    """Upgrade pip"""
    with virtualenv():
        run('pip install --upgrade pip')


@task
def create_media_dir():
    """Create `media` dir"""
    with cd(env.project_root):
        run('mkdir -p -m 775 media')


@task
def create_logs():
    """Create `logs` dir and log files"""
    with cd(env.project_root):
        run('mkdir -p -m 775 logs')
        run('touch logs/debug.log')
        run('touch logs/access.log')
        run('touch logs/error.log')
        run('chmod 664 logs/debug.log')


@task
def clear_logs():
    """Clear debug logs"""
    with cd(env.project_root):
        run("echo '' > logs/access.log")
        run("echo '' > logs/debug.log")
        run("echo '' > logs/error.log")
