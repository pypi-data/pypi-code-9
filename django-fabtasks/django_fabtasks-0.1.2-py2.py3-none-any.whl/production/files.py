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
from fabric.contrib import project
from fabric.contrib.console import confirm

from fabtasks.context import virtualenv

# -----------------------------------------------------------------------------


@task
def collect_static():
    """Collect static files"""
    with virtualenv():
        run('./manage.py collectstatic')


@task
def copy_static():
    """Copy remote static files to local"""
    if confirm('Are you sure, this will overwrite local static files?', default=False):
        project.rsync_project(
            local_dir=env.local_static_root,
            remote_dir=env.static_root,
            delete=False,
            upload=False  # pull files from server
        )


@task
def copy_media():
    """Copy remote media files to local"""
    if confirm('Are you sure, this will overwrite local media files?', default=False):
        project.rsync_project(
            local_dir=env.local_media_root,
            remote_dir=env.media_root,
            delete=False,
            upload=False  # pull files from server
        )


@task()
def delete_unused():
    """Delete unused media files"""
    if confirm('Are you sure, this will permanently delete various remote media files?', default=False):
        with virtualenv():
            run('./manage.py unreferenced_files | xargs -I{} rm -v {}')


@task
def delete_pyc():
    """Delete pyc files"""
    with virtualenv():
        run('./manage.py clean_pyc')


@task
def fix_permissions():
    """Ensure proper permissions on project folders"""
    with cd(env.project_root):
        # Change group on entire project
        run('chown -R :{group} {project_root}'.format(
            group=env.group,
            project_root=env.project_root))

        # Enable full perms for user/group only on all folders recursively in media
        run('find {media_root} -type d -print0 | xargs -0 chmod 775'.format(
            media_root=env.media_root))

        # Enable normal file perms on all files recursively in media
        run('find {media_root} -type f -print0 | xargs -0 chmod 644'.format(
            media_root=env.media_root))

        # Enable read/write for user/group on all files recursively in logs
        run('chmod 775 logs/')
        run('find logs/ -type f -print0 | xargs -0 chmod 664')
