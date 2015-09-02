# -*- coding: utf-8 -*-
"""
.. module:: TODO
   :platform: Unix
   :synopsis: TODO.

.. moduleauthor:: Aljosha Friemann <aljosha.friemann@gmail.com>

"""

import logging

from sh import git, ErrorReturnCode

logging.getLogger('sh').setLevel(logging.WARNING)

from . import core, utils, file_utils, exceptions

class Storage(core.FileHandler):
    """Storage

    :param storage_dir: the directory where files should be stored
    """

    def __init__(self, storage_dir):
        super(Storage, self).__init__(storage_dir)
        self._git = git.bake('--git-dir=%s/.git' % storage_dir,
                             '--work-tree=%s' % storage_dir)
        try:
            self.git(['status'])
        except exceptions.GitCommandException as e:
            if e.exit_code == 128:
                self.git(['init'])
                self.git(['config', 'branch.autosetuprebase', 'always'])
                self.git(['config', 'remote.origin.push', 'HEAD'])
            else:
                raise

    def _add(self, path, new_path, force):
        """_add

        :param path: to path to be stored
        :param new_path: the path where the file should be stored
        :param force: if existing files should be overwritten
        """
        file_utils.copy(path, new_path, force)
        self._git('add', new_path)

    def _move(self, path, new_path, force):
        """_move

        :param path: to original file path
        :param new_path: the new path
        :param force: if existing files should be overwritten
        """
        self._git('mv', path, new_path)

    def git(self, args, fg=False):
        """git

        :param args:
        :param fg:
        """
        self._logger.debug("git command: %s" % list(args))
        try:
            return self._git(list(args), _out=utils.stdout if fg else None).strip()
        except ErrorReturnCode as e:
            raise exceptions.GitCommandException(e.full_cmd.strip(),
                                                 e.stdout.decode().strip(),
                                                 e.stderr.decode().strip(),
                                                 e.exit_code)

    def branch(self):
        """branch"""
        return self.git(['symbolic-ref', '--short', 'HEAD'])

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
