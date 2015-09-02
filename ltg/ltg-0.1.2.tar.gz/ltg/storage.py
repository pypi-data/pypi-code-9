# -*- coding: utf-8 -*-
"""
.. module:: TODO
   :platform: Unix
   :synopsis: TODO.

.. moduleauthor:: Aljosha Friemann <aljosha.friemann@gmail.com>

"""

import logging

from sh import git, ErrorReturnCode_128
logging.getLogger('sh').setLevel(logging.WARNING)

from . import core, file_utils, exceptions

class Storage(core.FileHandler):
    """Storage"""

    def __init__(self, storage_dir):
        super(Storage, self).__init__(storage_dir)
        self._git = git.bake('--git-dir=%s/.git' % storage_dir,
                             '--work-tree=%s' % storage_dir)
        try:
            self.git('status')
        except ErrorReturnCode_128:
            self.git('init')

    def _add(self, path, new_path, force):
        """single_add

        :param path:
        :param new_path:
        :param force:
        """
        file_utils.copy(path, new_path, force)
        self._git('add', new_path)

    def _move(self, path, new_path, force):
        """move

        :param path:
        :param new_path:
        :param force:
        """
        self._git('mv', path, new_path)

    def git(self, *args):
        self._logger.debug("git command: %s" % list(args))
        return self._git(*args)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
