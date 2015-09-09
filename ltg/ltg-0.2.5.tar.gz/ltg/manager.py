#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
.. module:: TODO
   :platform: Unix
   :synopsis: TODO.

.. moduleauthor:: Aljosha Friemann <aljosha.friemann@gmail.com>

"""

import os, logging

from . import file_utils, storage, linker, git, exceptions

################################################################################

log = logging.getLogger(__name__)

class Manager():
    """Manager

    :storage_dir: the directory where files should be stored
    :linker_dir: the directory where stored files should be linked to
    """
    def __init__(self, storage_dir, linker_dir):
        self._storage = storage.Storage(storage_dir)
        self._linker = linker.Linker(linker_dir)
        self._git = git.Git(storage_dir)

    def storage_dir(self):
        """storage_dir"""
        return self._storage.root()

    def linker_dir(self):
        """linker_dir"""
        return self._linker.root()

    def get_category(self, path):
        """get_category

        :param path:
        """
        if not self._storage.owns(path):
            raise exceptions.NoOwnedFileException(path)
        return path.replace(self.storage_dir(), '').split('/')[1]

    def get_categories(self):
        """get_categories

        :returns: absolute paths to all categories
        """
        for directory in os.listdir(self.storage_dir()):
            if not directory.startswith('.'):
                yield directory

    def get_category_files(self, category):
        """get_category_files

        :param category: the path to the requested category
        :returns: generator object for all files in categories
        """
        for root,dirs,files in os.walk(os.path.join(self.storage_dir(), category)):
            dirs[:] = [ d for d in dirs if d != '.git' ]

            for d in dirs:
                yield os.path.join(root, d)

            for f in files:
                yield os.path.join(root, f)

            break

    def owns(self, path):
        """owns

        TODO

        :path: a path to an existing file.
        :returns: boolean if path belongs to FileHandler.

        """
        return (self._storage.owns(path) and self._linker.owns(path))

    def store(self, paths, relative_to, category, force):
        """store

        TODO

        :path: a path to an existing file.

        """
        if relative_to is None:
            relative_to = self.linker_dir()

        base_dir = os.path.join(self.storage_dir(), category)

        # TODO committing
        for path in paths:
            new_path = file_utils.get_target_path(base_dir,
                                                  path,
                                                  relative_to)

            self._storage.add(path, new_path, force)
            self._git('add', new_path)

    def link(self, force):
        """link

        TODO

        :param force: if existing files should be overwritten

        """
        for category in self.get_categories():
            for f in self.get_category_files(category):
                link_path = file_utils.get_target_path(self.linker_dir(),
                                                       f,
                                                       os.path.join(self.storage_dir(),
                                                                    category))

                self._linker.add(f, link_path, force)

    def move(self, files, destination, force):
        """TODO: Docstring for move.

        TODO: split this up somehow?

        :path: a path to an existing (owned) file.
        :new_path: the new path.

        """
        directory = os.path.isdir(destination) or len(files) > 1

        for f in files:
            if os.path.isdir(f):
                raise NotImplementedError("moving directories")

            if self._linker.owns(f):
                real_path = os.path.realpath(f)
                category = self.get_category(real_path)

                if directory:
                    new_storage_dir = file_utils.get_target_path('%s/%s' % (self.storage_dir(), category),
                                                                  destination,
                                                                  self.linker_dir())
                    file_utils.makedir(destination)
                    file_utils.makedir(new_storage_dir)

                    new_storage_path = os.path.join(new_storage_dir, os.path.basename(f))
                    new_linker_path = os.path.join(destination, os.path.basename(f))
                else:
                    new_storage_path = file_utils.get_target_path('%s/%s' % (self.storage_dir(), category),
                                                                  destination,
                                                                  self.linker_dir())
                    new_linker_path = destination

                self._git.move(real_path, new_storage_path)

                self._linker.move(f, new_linker_path, force)
                self._linker.update_link(new_linker_path,
                                         new_storage_path)

                if file_utils.is_empty(os.path.dirname(real_path)):
                    file_utils.remove(os.path.dirname(real_path))
            elif self._git.owns(f):
                raise NotImplementedError("move indexed files")
            elif self._storage.owns(f):
                raise NotImplementedError("move stored files not in git index")
            else:
                raise exceptions.NoOwnedFileException(f)

    def remove(self, path, recursive, force):
        """TODO: Docstring for remove.

        :path: a path to an existing file.

        """
        raise NotImplementedError("remove")

    def unlink(self, files):
        """unlink

        :param path:
        """
        raise NotImplementedError("unlink")

    def sync_up(self):
        """sync_up"""
        try:
            self._git('commit', '-am', 'automatic commit before sync up')
        except exceptions.GitCommandException as e:
            if e.exit_code != 1:
                raise
        self._git('push', 'origin', self._git.branch(), foreground=True)

    def sync_down(self):
        """sync_down"""
        self._git('stash')
        self._git('pull', 'origin', self._git.branch(), foreground=True)

        if len(self._git('stash', 'list')[0]) > 0:
            self._git('stash', 'pop')

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
