# -*- coding: utf-8 -*-
"""
.. module:: TODO
   :platform: Unix
   :synopsis: TODO.

.. moduleauthor:: Aljosha Friemann <aljosha.friemann@gmail.com>

"""

import logging

from . import core, utils, file_utils, exceptions, git

################################################################################

class Storage(core.FileHandler):
    """Storage

    :param storage_dir: the directory where files should be stored
    """

    def _add(self, path, new_path, force):
        """_add

        :param path: to path to be stored
        :param new_path: the path where the file should be stored
        :param force: if existing files should be overwritten
        """
        file_utils.copy(path, new_path, force)

    def _move(self, path, new_path, force):
        """_move

        :param path: to original file path
        :param new_path: the new path
        :param force: if existing files should be overwritten
        """
        file_utils.move(path, new_path, force)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
