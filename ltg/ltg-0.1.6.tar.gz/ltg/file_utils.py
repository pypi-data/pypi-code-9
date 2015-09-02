# -*- coding: utf-8 -*-
"""
.. module:: TODO
   :platform: Unix
   :synopsis: TODO.

.. moduleauthor:: Aljosha Friemann <aljosha.friemann@gmail.com>

"""

import os, shutil, logging

from . import exceptions

log = logging.getLogger(__name__)

def get_target_path(base, path, relative_to):
    """
    TODO: Docstring for get_target_path.
    TODO: better name

    >>> get_target_path('/abc/def', '/home/lala/abc/1234', '/home')
    '/abc/def/lala/abc/1234'

    >>> get_target_path('/abc/def', '/abc/def/lala/123', '/home')
    Traceback (most recent call last):
    ...
    NoPrefixException: ('/home', '/abc/def/lala/123')

    >>> get_target_path('/abc/def', '/home/lala/123', '/var')
    Traceback (most recent call last):
    ...
    NoPrefixException: ('/var', '/home/lala/123')

    :param path:
    :param relative_to:

    """
    if not is_prefix(relative_to, path):
        raise exceptions.NoPrefixException(relative_to, path)

    return os.path.join(base, path.replace(relative_to, '').lstrip('/'))

def filetype(path):
    """filetype

    :param path:
    """
    if os.path.exists(path):
        if os.path.isdir(path):
            return 'directory'
        elif os.path.islink(path):
            return 'link'
        elif os.path.isfile(path):
            return 'file'
        else:
            return 'unkown'
    elif os.path.islink(path):
        return 'broken link'

def is_prefix(prefix, path):
    """is_prefix

    >>> is_prefix('/', '/')
    True

    >>> is_prefix('/var', '/foo/bar')
    False

    >>> is_prefix('/', '/foo/bar')
    True

    >>> is_prefix('/var', '/var/abc')
    True

    :param prefix:
    :param path:
    """
    return (os.path.commonprefix([prefix, path]) == prefix)

def is_broken_symlink(path):
    """is_broken_symlink

    :param path:
    """
    return not os.path.exists(os.readlink(path))

def link_file(target, path, force):
    """link

    :target:
    :path:
    :force:
    """
    if os.path.exists(path):
        if os.path.samefile(target, path):
            return

        elif not force:
            raise exceptions.FileExistsError(path)
        else:
            os.remove(path)

    makedir(os.path.dirname(path))

    log.debug('linking file %s to %s', target, path)

    os.symlink(target, path)

def link_directory(target, path, force):
    """_link_directory

    :param target:
    :param path:
    :param force:
    """
    log.debug("linking directory %s to %s", target, path)

    for root,dirs,files in os.walk(target):
        dirs[:] = [ d for d in dirs if d != '.git' ]

        new_root = get_target_path(path, root, target)

        makedir(new_root)

        for f in files:
            link_file(os.path.join(root, f), os.path.join(new_root, f), force)

def link(target, path, force):
    """link

    :param target:
    :param path:
    :param force:
    """
    if os.path.isdir(target):
        link_directory(target, path, force)
    else:
        link_file(target, path, force)

def remove(path):
    """remove.

    :path:
    """
    if os.path.exists(path) or os.path.islink(path):
        log.debug('removing %s in %s', filetype(path), path)

        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)

def move(src, dst, force):
    """move

    :param src:
    :param dst:
    :param force:
    """
    if os.path.exists(dst):
        if not force:
            raise exceptions.FileExistsError(dst)
        else:
            os.remove(dst)

    log.debug('moving %s from %s to %s', filetype(src), src, dst)

    shutil.move(src, dst)

def copy(src, dst, force):
    """copy

    :param src:
    :param dst:
    :param force:
    """
    if os.path.exists(dst):
        if not force:
            raise exceptions.FileExistsError(dst)
        else:
            os.remove(dst)

    log.debug('copying %s from %s to %s', filetype(src), src, dst)

    makedir(os.path.dirname(dst))

    if os.path.isdir(src):
        shutil.copytree(src, dst)
    else:
        shutil.copy(src, dst)

def makedir(path, force = False):
    """makedir

    :param path:
    :param force:
    """
    if os.path.exists(path):
        if os.path.isdir(path):
            return

        elif not force:
            raise exceptions.FileExistsError(path)
        else:
            os.remove(path)

    log.debug('creating directory %s' % path)

    os.makedirs(path)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
