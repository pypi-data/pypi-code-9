# -*- coding: utf-8 -*-
"""
.. module:: TODO
   :platform: Unix
   :synopsis: TODO.

.. moduleauthor:: Aljosha Friemann <aljosha.friemann@gmail.com>

"""

import logging

from . import exceptions, file_utils

log = logging.getLogger(__name__)

def user_confirms(prompt):
    return input(prompt + ' [y]/n ') in ['','y','Y','yes']

def ensure_directory(path, interactive=False):
    if not os.path.exists(path):
        if interactive and not user_confirms('%s does not exist, want to create it?' % path):
            return False

        file_utils.makedir(path)
    return True

def fullname(o):
  return o.__module__ + "." + o.__class__.__name__

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
