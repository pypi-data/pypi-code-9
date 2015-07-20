# coding: utf-8
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from abc import ABCMeta, abstractmethod

from six import add_metaclass


@add_metaclass(ABCMeta)
class BaseRepository(object):

    def clear_caches(self):
        """Should clear any caches used by the implementation."""

    @abstractmethod
    def find_best_match(self, ireq):
        """
        Return a Version object that indicates the best match for the given
        InstallRequirement according to the repository.
        """

    @abstractmethod
    def get_dependencies(self, ireq):
        """
        Given a pinned or an editable InstallRequirement, returns a set of
        dependencies (also InstallRequirements, but not necessarily pinned).
        They indicate the secondary dependencies for the given requirement.
        """
