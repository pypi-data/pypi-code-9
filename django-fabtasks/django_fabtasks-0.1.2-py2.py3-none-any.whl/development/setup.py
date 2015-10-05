# -*- coding: utf-8 -*-

# Copyright 2015
#
# This file is part of proprietary software and use of this file
# is strictly prohibited without written consent.
#
# @author  Tim Santor  <tsantor@xstudios.agency>

# -----------------------------------------------------------------------------

import os

# 3rd Party
from fabric.api import *

# -----------------------------------------------------------------------------


def create_local_settings():
    """Create default local settings file"""
    if os.path.exists('{package}/settings/local_settings_example.py'.format(package=env.package_name)):
        local('cp {package}/settings/local_settings_example.py {package}/settings/local_settings.py'.format(package=env.package_name))
        local('rm {package}/settings/local_settings_example.py'.format(package=env.package_name))


def create_virtualenv():
    """Create and active a virtual environment"""
    local('virtualenv %s' % env.virtualenv_dir)
    local('source %s/bin/activate' % env.virtualenv_dir)


@task
def pip_install_requirements():
    """Install pip requirements from requirements.txt"""
    local('pip install -r requirements.txt')


@task
def pip_update():
    """Upgrade pip"""
    local('pip install --upgrade pip')


@task
def pip_update_packages():
    """Update outdated pip packages (Be careful!)"""
    local("./manage.py pipchecker | awk '{print $1}' | xargs pip install -U")


@task
def create_media_dir():
    """Create `media` dir"""
    local('mkdir -p -m 775 media')


@task
def create_logs():
    """Create `logs` dir and log files"""
    local('mkdir -p -m 775 logs')
    local('touch logs/debug.log')
    local('touch logs/access.log')
    local('touch logs/error.log')
    local('chmod 664 logs/debug.log')


@task
def clear_logs():
    """Clear debug logs"""
    local("echo '' > logs/access.log")
    local("echo '' > logs/debug.log")
    local("echo '' > logs/error.log")
