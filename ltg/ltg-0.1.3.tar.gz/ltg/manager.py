#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
.. module:: TODO
   :platform: Unix
   :synopsis: TODO.

.. moduleauthor:: Aljosha Friemann <aljosha.friemann@gmail.com>

"""

import os, logging

from . import file_utils, storage, linker

log = logging.getLogger(__name__)

class Manager():
    def __init__(self, storage_dir, linker_dir):
        """TODO: Docstring for __init__.

        :storage: TODO
        :linker: TODO
        :returns: TODO

        """
        self._storage = storage.Storage(storage_dir)
        self._linker = linker.Linker(linker_dir)

    def git(self, *args):
        return self._storage.git(*args)

    def storage_dir(self):
        """storage_dir"""
        return self._storage.root()

    def linker_dir(self):
        """linker_dir"""
        return self._linker.root()

    def get_categories(self):
        for directory in os.listdir(self.storage_dir()):
            if not directory.startswith('.'):
                yield os.path.join(self.storage_dir(), directory)

    def get_category_files(self, category):
        for root,dirs,files in os.walk(category):
            dirs[:] = [ d for d in dirs if d != '.git' ]

            for d in dirs:
                yield os.path.join(root, d)

            for f in files:
                yield os.path.join(root, f)

            # TODO break?
            break

    def owns(self, path):
        """TODO: Docstring for owns.

        :path: a path to an existing file.
        :returns: boolean if path belongs to FileHandler.

        """
        return (self._storage.owns(path) and self._linker.owns(path))

    def store(self, paths, relative_to, category, force):
        """TODO: Docstring for link.

        :path: a path to an existing file.
        :returns: the path of the file in storage.

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

        :param path:
        :param force:
        :returns: the path of the created link

        """
        for category in self.get_categories():
            for f in self.get_category_files(category):
                link_path = file_utils.get_target_path(self.linker_dir(),
                                                       f,
                                                       category)

                self._linker.add(f, link_path, force)

    def move(self, path, new_path, force):
        """TODO: Docstring for move.

        :path: a path to an existing (owned) file.
        :new_path: the new path.
        :returns: the new path.

        """
        # TODO think about this
        try:
            return self._linker.move(path, new_path, force)
        except exceptions.NoOwnedFileException:
            return self._storage.move(path, new_path, force)

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

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
