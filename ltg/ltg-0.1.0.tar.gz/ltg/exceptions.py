#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
.. module:: TODO
   :platform: Unix
   :synopsis: TODO.

.. moduleauthor:: Aljosha Friemann <aljosha.friemann@gmail.com>

"""

class LTGException(Exception):
    pass

class MissingDirectoryException(LTGException):
    pass

class NoPrefixException(LTGException):
    pass

class NonRecursiveException(LTGException):
    pass

class LinkException(LTGException):
    pass

class NoOwnedFileException(LTGException):
    pass

class NoStoredFileException(LTGException):
    pass

class NoCategoryException(LTGException):
    pass

class GitCommandException(LTGException):
    pass

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
