#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
.. module:: TODO
   :platform: Unix
   :synopsis: TODO.

.. moduleauthor:: Aljosha Friemann <aljosha.friemann@gmail.com>

"""

import logging

from . import core, file_utils, exceptions

class Linker(core.FileHandler):
    """Linker"""

    def _add(self, path, new_path, force):
        """_add

        :param path:
        :param new_path:
        :param recursive:
        :param force:
        """
        file_utils.link(path, new_path, force)

    def _move(self, path, new_path, force):
        """move

        :param path:
        :param new_path:
        :param new_target:
        :param force:
        """
        file_utils.move(path, new_path, force)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
