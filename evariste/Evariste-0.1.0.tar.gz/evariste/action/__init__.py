# Copyright Louis Paternault 2015
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Actions performed to compile files."""

import logging
import os

from evariste import errors, plugins

LOGGER = logging.getLogger(__name__)

################################################################################
# Actions

class PathCompiler:
    """Compiler of one path.

    The main difference between this object and :class:`Action` is that:
        - there is one instance of :class:`Action` for the whole tree;
        - there is one instance of :class:`PathCompiler` per path.
    """
    # pylint: disable=too-few-public-methods

    def __init__(self, parent, path, plugin_id, shared):
        self.shared = shared
        self.plugin_id = plugin_id
        self.path = path
        self.parent = parent

    def compile(self):
        """Perform actual compilation of `self.path`."""
        raise NotImplementedError()

class Action(plugins.PluginBase):
    """Generic action"""
    # pylint: disable=too-many-instance-attributes, too-few-public-methods

    plugin_type = "action"
    pathcompiler = PathCompiler

    def compile(self, path):
        """Compile ``path``, catching :class:`EvaristeError` exceptions.

        This function *must* be thread-safe.
        """
        try:
            return self.pathcompiler(self, path, self.plugin_id, self.shared).compile()
        except errors.EvaristeError as error:
            LOGGER.error(str(error))
            return Report(
                path,
                success=False,
                error=str(error),
                log=[LogInternal(str(error))],
                )

class DirectoryCompiler(PathCompiler):
    """Compiler of a directory."""

    def compile(self):
        return Report(
            self.path,
            success=self.success(),
            error="At least one file in this directory failed.",
            target=None,
            )

    def success(self):
        """Return ``True`` if compilation of all subpath succeeded."""
        for sub in self.path:
            if not self.path[sub].report.success:
                return False
        return True


class DirectoryAction(Action):
    """Fake action on directories."""
    # pylint: disable=abstract-method, too-few-public-methods

    keyword = "directory"
    pathcompiler = DirectoryCompiler
    required = True

    def match(self, dummy):
        return False

################################################################################
# Reports

class Report:
    """Report of an action. Mainly a namespace with very few methods."""

    def __init__(
            self,
            path,
            target=None,
            error="Undocumented error",
            success=False,
            log=None,
            depends=None,
        ):
        # pylint: disable=too-many-arguments

        self.depends = depends
        if self.depends is None:
            self.depends = set()

        self.log = log
        if self.log is None:
            self.log = []

        self.path = path
        self.target = target
        self._success = success
        self.error = error

    @property
    def full_depends(self):
        """Set of files this action depends on, including ``self.path``."""
        return self.depends | set([self.path.from_fs])

    @property
    def success(self):
        """Success getter"""
        return self._success

    @success.setter
    def success(self, value):
        """Success setter."""
        self._success = value




################################################################################
# Log

class Log:
    """Action log"""
    # pylint: disable=too-few-public-methods

    def __init__(self, identifier, content):
        self.identifier = identifier
        self.content = content

    def __str__(self):
        return "({}) {}".format(self.identifier, self.content)

class LogInternal(Log):
    """Log of internal exception"""
    # pylint: disable=too-few-public-methods

    def __init__(self, content):
        super().__init__("Internal error", content)

class LogFile(Log):
    """Log from file"""
    # pylint: disable=too-few-public-methods

    def __init__(self, filename):
        with open(filename, errors="replace") as file:
            super().__init__(filename, file.read())

class LogPipe(Log):
    """Log from pipe"""
    # pylint: disable=too-few-public-methods

    IDENTIFIERS = {
        0: "standard input", # Why would one do that?
        1: "standard output",
        2: "standard error",
        }

    def __init__(self, pipe, content=""):
        super().__init__(self.IDENTIFIERS.get(pipe, str(pipe)), content)

    def read(self, pipe):
        """Read content from pipe."""
        with os.fdopen(pipe, errors="replace") as file:
            for line in file:
                self.content += line

class MultiLog(Log):
    """List of logs"""
    # pylint: disable=too-few-public-methods

    def __init__(self, sublogs):
        super().__init__("multilog", "")
        self._sublogs = sublogs

    def __iter__(self):
        yield from self._sublogs

