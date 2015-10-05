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

from fabtasks.context import virtualenv

# -----------------------------------------------------------------------------


@task
def migrate():
    """Apply migrations"""
    with virtualenv():
        run('./manage.py migrate')


@task
def reset():
    """Reset database"""
    if confirm('Are you sure, this will delete the remote database?', default=False):
        with virtualenv():
            run('./manage.py reset_db')


@task
def createsuperuser():
    """Create superuser"""
    with virtualenv():
        run('./manage.py createsuperuser')


@task
def dump_mysql():
    """Perform a MySQL dump of the database"""
    filename = '{}_{}.sql'.format(env.db_name, time.strftime('%Y%m%d%H%M%S'))
    with cd(env.project_root):
        run('mysqldump -u {user} -p {db_name} > {filename}'.format(
            user=env.db_user,
            db_name=env.db_name,
            filename=filename))


@task
def import_mysql(filename):
    """Perform a MySQL import of the database"""
    with cd(env.project_root):
        run('mysql -u {user} -p {db_name} < {db_name}.sql'.format(
            user=env.db_user,
            db_name=env.db_name,
            filename=filename))
        run('rm {}'.format(filename))


@task
def copy_mysql():
    """Perform a remote MySQL dump and import it on the local machine"""
    if confirm('Are you sure, this will overwrite the local database?', default=False):
        filename = '{}_{}.sql'.format(env.db_name, time.strftime('%Y%m%d%H%M%S'))
        with cd(env.project_root):
            run('mysqldump -u {user} -p {db_name} > {filename}'.format(
                user=env.db_user,
                db_name=env.db_name,
                filename=filename))
            get(remote_path=filename, local_path=filename)
            run('rm {}'.format(filename))

        local('mysql -u {user} -p {db_name} < {filename}'.format(
            user=env.db_user,
            db_name=env.db_name,
            filename=filename))
        local('rm {}'.format(filename))
