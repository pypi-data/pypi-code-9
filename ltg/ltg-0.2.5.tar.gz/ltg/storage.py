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

    def _clean(self):
        """_clean

        TODO: this propably won't work and should be well thought out. However, an automatic cleanup process would be
              very useful

        """
        for root, dirs, files in os.walk(self._root_dir):
            for d in dirs:
                abspath = os.path.join(root, d)
                if file_utils.is_empty(abspath):
                    file_utils.remove(abspath)
                    dirs.remove(d)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
