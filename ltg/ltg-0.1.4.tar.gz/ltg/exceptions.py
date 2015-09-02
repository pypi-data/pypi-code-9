#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
.. module:: TODO
   :platform: Unix
   :synopsis: TODO.

.. moduleauthor:: Aljosha Friemann <aljosha.friemann@gmail.com>

"""

class FileExistsError(Exception):
    """FileExistsError
    exists to avoid problems with python2
    """
    pass

class LTGException(Exception):
    """LTGException"""
    pass

class MissingDirectoryException(LTGException):
    """MissingDirectoryException"""
    pass

class NoPrefixException(LTGException):
    """NoPrefixException"""
    pass

class NonRecursiveException(LTGException):
    """NonRecursiveException"""
    pass

class LinkException(LTGException):
    """LinkException"""
    pass

class NoOwnedFileException(LTGException):
    """NoOwnedFileException"""
    pass

class NoStoredFileException(LTGException):
    """NoStoredFileException"""
    pass

class NoCategoryException(LTGException):
    """NoCategoryException"""
    pass

class GitCommandException(LTGException):
    """GitCommandException"""
    pass

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
