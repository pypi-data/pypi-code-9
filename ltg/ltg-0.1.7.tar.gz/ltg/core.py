#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
.. module:: TODO
   :platform: Unix
   :synopsis: TODO.

.. moduleauthor:: Aljosha Friemann <aljosha.friemann@gmail.com>

"""

import os, logging

from abc import ABCMeta, abstractmethod

from . import utils, file_utils, exceptions

class FileHandler(object):
    """FileHandler

    :param root:
    """

    def __init__(self, root):
        self._logger = logging.getLogger(utils.fullname(self))
        self._root_dir = root
        file_utils.makedir(self._root_dir)

    def check(self):
        """check"""
        self._logger.debug('checking')

        if not os.path.exists(self._root_dir):
            raise exceptions.MissingDirectoryException(self._root_dir)
        elif not os.path.isdir(self._root_dir):
            raise exceptions.FileExistsError(self._root_dir)

    def root(self):
        """root"""
        return self._root_dir

    def owns(self, path):
        """owns_path

        :param path:
        """
        self._logger.debug('checking if "%s" is owned path', path)

        return file_utils.is_prefix(self._root_dir, path)

    def add(self, path, new_path, force):
        """add

        :param path:
        :param new_path:
        :param force:
        """
        self._logger.debug('adding %s to %s', path, new_path)

        if not self.owns(new_path):
            raise exceptions.NoOwnedFileException(new_path)

        self._add(path, new_path, force)

        return new_path

    def move(self, path, new_path, force):
        """TODO: Docstring for move.

        :param path: a path to an existing (owned) file.
        :param new_path: the new path.
        :returns: the new path.

        """
        if not self.owns(path):
            raise exceptions.NoOwnedFileException(path)
        elif not self.owns(new_path):
            raise exceptions.NoOwnedFileException(new_path)

        self._move(path, new_path, force)

        return new_path

    def remove(self, path, recursive):
        """remove

        :param path:
        :param recursive:
        """
        if not self.owns(path):
            raise exceptions.NoOwnedFileException(path)

        self._remove(path, recursive)

        return path

    @abstractmethod
    def _add(self, path, new_path, force):
        """TODO: Docstring for link.

        :param path: a path to an existing file.
        :param new_path: a path to an existing file.
        :returns: the path of the resulting (owned) file.
        """
        raise NotImplementedError("_add in %s" % self.__class__.__name__)

    @abstractmethod
    def _move(self, path, new_path, force):
        """_move

        :param path:
        :param new_path:
        :param force:
        """
        raise NotImplementedError("_move in %s" % self.__class__.__name__)

    @abstractmethod
    def _remove(self, path, recursive):
        """_remove

        :param path:
        :param recursive:
        """
        raise NotImplementedError("_remove in %s" % self.__class__.__name__)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
