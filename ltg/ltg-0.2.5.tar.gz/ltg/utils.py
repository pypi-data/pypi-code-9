# -*- coding: utf-8 -*-
"""
.. module:: TODO
   :platform: Unix
   :synopsis: TODO.

.. moduleauthor:: Aljosha Friemann <aljosha.friemann@gmail.com>

"""

import logging, sys

from . import exceptions, file_utils

################################################################################

log = logging.getLogger(__name__)

def user_confirms(prompt):
    """user_confirms

    :param prompt: the message prompt
    :returns: True if user input is empty or equal to 'y', 'Y' or 'yes'
    """
    return input(prompt + ' [y]/n ') in ['','y','Y','yes']

def ensure_directory(path, interactive=False):
    """ensure_directory

    :param path: the supposed directory
    :param interactive: if user interaction should be required to create the directory
    :returns: True if path is a directory, else False
    """
    if not os.path.exists(path):
        if interactive and not user_confirms('%s does not exist, want to create it?' % path):
            return False

        file_utils.makedir(path)
    return True

def fullname(o):
    """fullname

    :param o: an object
    :returns: the fully qualified object name
    """
    return o.__module__ + "." + o.__class__.__name__

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
