#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
.. module:: TODO
   :platform: Unix
   :synopsis: TODO.

.. moduleauthor:: Aljosha Friemann <aljosha.friemann@gmail.com>

"""

import os, logging

from . import file_utils, storage, linker, exceptions

log = logging.getLogger(__name__)

class Manager():
    """Manager

    :storage_dir: the directory where files should be stored
    :linker_dir: the directory where stored files should be linked to
    """
    def __init__(self, storage_dir, linker_dir):
        self._storage = storage.Storage(storage_dir)
        self._linker = linker.Linker(linker_dir)

    def git(self, args, fg=False):
        """git

        :param args: arguments to git
        :returns: the git command standard output
        """
        return self._storage.git(args, fg)

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

            # TODO break?
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
                                                  os.path.abspath(path),
                                                  relative_to)

            self._storage.add(path, new_path, force)

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

    def move(self, path, new_path, force):
        """TODO: Docstring for move.

        :path: a path to an existing (owned) file.
        :new_path: the new path.

        """
        if os.path.isdir(path):
            raise NotImplementedError("moving directories")

        if self._linker.owns(path):
            real_path = os.path.realpath(path)
            category = self.get_category(real_path)
            new_storage_path = file_utils.get_target_path('%s/%s' % (self.storage_dir(), category),
                                                          new_path,
                                                          self.linker_dir())

            self._storage.move(real_path, new_storage_path, force)

            self._linker.move(path, new_path, force)
            self._linker.update_link(new_path, new_storage_path)
        elif self._storage.owns(path):
            raise NotImplementedError("move stored files")
            return self._storage.move(path, new_path, force)
        else:
            raise exceptions.NoOwnedFileException(path)

    def remove(self, path, recursive, force):
        """TODO: Docstring for remove.

        :path: a path to an existing file.

        """
        raise NotImplementedError("remove")

        self._linker.remove(path, recursive)

        storage_path = None # TODO

        self._storage.remove(storage_path, recursive)

    def unlink(self, files):
        """unlink

        :param path:
        """
        raise NotImplementedError("unlink")

        self._linker.remove(path)

        stored_file = self._storage.get_target_path(path, self.linker_dir)

        file_utils.copy(stored_file, path)

    def sync_up(self):
        """sync_up"""
        self.git(['push', 'origin', self._storage.branch()])

    def sync_down(self):
        """sync_down"""
        try:
            self.git(['commit', '-am', 'automatic commit before sync down'])
        except exceptions.GitCommandException as e:
            if e.exit_code != 1:
                raise
        self.git(['pull', 'origin', self._storage.branch()])

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
