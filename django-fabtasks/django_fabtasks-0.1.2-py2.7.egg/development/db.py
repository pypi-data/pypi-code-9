# -*- coding: utf-8 -*-

# Copyright 2015
#
# This file is part of proprietary software and use of this file
# is strictly prohibited without written consent.
#
# @author  Tim Santor  <tsantor@xstudios.agency>

# -----------------------------------------------------------------------------

import time

# 3rd Party
from fabric.api import *
from fabric.contrib.console import confirm

# -----------------------------------------------------------------------------


@task
def makemigrations():
    """Make migrations"""
    local('./manage.py makemigrations')


@task
def migrate():
    """Apply migrations"""
    local('./manage.py migrate')


@task
def reset():
    """Reset the entire DB (Truncate all tables)"""
    local('./manage.py reset_db')


@task
def createsuperuser():
    """Create a new superuser"""
    local('./manage.py createsuperuser')


@task
def dump_mysql():
    """Perform a MySQL dump of the database"""
    filename = '{}_{}.sql'.format(env.db_name, time.strftime('%Y%m%d%H%M%S'))
    local('mysqldump -u {user} -p {db_name} > {filename}'.format(
        user=env.db_user,
        db_name=env.db_name,
        filename=filename))


@task
def import_mysql(filename):
    """Perform a MySQL import of the database"""
    local('mysql -u {user} -p {db_name} < {db_name}.sql'.format(
        user=env.db_user,
        db_name=env.db_name,
        filename=filename))
    local('rm {}'.format(filename))


@task
def copy_mysql():
    """Perform a local MySQL dump and import it on the remote machine"""
    if confirm('Are you sure, this will overwrite the remote database?', default=False):
        filename = '{}_{}.sql'.format(env.db_name, time.strftime('%Y%m%d%H%M%S'))
        local('mysqldump -u {user} -p {db_name} > {filename}'.format(
            user=env.db_user,
            db_name=env.db_name,
            filename=filename))
        put(local_path=filename, remote_path=env.project_root)
        local('rm {}'.format(filename))

        with cd(env.project_root):
            run('mysql -u {user} -p {db_name} < {filename}'.format(
                user=env.db_user,
                db_name=env.db_name,
                filename=filename))
            run('rm {}'.format(filename))
