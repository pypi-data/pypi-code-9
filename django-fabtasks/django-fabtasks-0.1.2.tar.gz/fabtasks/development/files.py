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

# -----------------------------------------------------------------------------


@task
def collect_static():
    """Collect static files"""
    local('./manage.py collectstatic')


@task
def copy_static():
    """Copy local static files to remote server"""
    if confirm('Are you sure, this will overwrite remote static files?', default=False):
        local('./manage.py collectstatic')
        project.rsync_project(
            local_dir=env.local_static_root,
            remote_dir=env.static_root,
            delete=False
        )


@task
def copy_media():
    """Copy local media files to remote server"""
    if confirm('Are you sure, this will overwrite remote media files?', default=False):
        project.rsync_project(
            local_dir=env.local_media_root,
            remote_dir=env.media_root,
            delete=False
        )


@task
def delete_media():
    """Delete all media files but preserve directories"""
    if confirm('Are you sure, this will permanently delete local media files?', default=False):
        local('find media -type f -print0 | xargs -0 rm')


@task()
def delete_unused():
    """Delete unused media files that are not referenced in the database"""
    if confirm('Are you sure, this will permanently delete various local media files?', default=False):
        local('./manage.py unreferenced_files | xargs -I{} rm -v {}')


@task
def delete_pyc():
    """Delete pyc files"""
    local('./manage.py clean_pyc')


@task
def fix_permissions():
    """Ensure proper permissions on project folders"""
    # Change group on entire project
    local('chown -R :{group} {project_root}'.format(
        group=env.local_group,
        project_root=env.local_project_root))

    # Enable full perms for user/group only on all folders recursively in media
    local('find {media_root} -type d -print0 | xargs -0 chmod 775'.format(
        media_root=env.local_media_root))

    # Enable normal file perms on all files recursively in media
    local('find {media_root} -type f -print0 | xargs -0 chmod 644'.format(
        media_root=env.local_media_root))

    # Enable read/write for user/group on all files recursively in logs
    local('chmod 775 logs/')
    local('find logs/ -type f -print0 | xargs -0 chmod 664')
