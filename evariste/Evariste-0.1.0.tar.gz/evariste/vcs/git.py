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

"""Access to git-versionned files."""

from datetime import datetime
import os
import pygit2

from evariste.vcs import VCS, NoRepositoryError

class Git(VCS):
    """Access git-versionned files"""
    # pylint: disable=no-member

    keyword = "git"

    def __init__(self, shared):
        super().__init__(shared)
        try:
            self.repository = pygit2.Repository(
                pygit2.discover_repository(
                    str(self.source)
                    )
                )
        except KeyError:
            raise NoRepositoryError(self.keyword, self.source)

        self._iter = None
        self._cached_mtime = None

    def walk(self):
        source = self.source.resolve().as_posix()
        for entry in self.repository.index:
            path = os.path.join(
                self.repository.workdir,
                entry.path,
                )
            if path.startswith(source):
                yield os.path.relpath(path, source)

    def is_versionned(self, path):
        return self.from_repo(path) in self.repository.index

    @property
    def workdir(self):
        return self.repository.workdir

    def _iter_start(self):
        """Initialize the commit iteration process."""
        self._iter = dict()
        self._iter["walker"] = self.repository.walk(
            self.repository.head.target,
            pygit2.GIT_SORT_TIME,
            )
        self._iter["commit"] = next(self._iter["walker"])

        self._cached_mtime = {
            entry.path: None
            for entry
            in self.repository.index
            }

    def _iter_walk(self):
        """Does one step of iterating over past commits, to set modification times"""
        old_commit = self._iter["commit"]
        self._iter["commit"] = next(self._iter["walker"])
        files_in_diff = (
            x.new_file_path
            for x in self._iter["commit"].tree.diff_to_tree(old_commit.tree)
            )
        for path in files_in_diff:
            if path in self._cached_mtime:
                if self._cached_mtime[path] is None:
                    self._cached_mtime[path] = datetime.fromtimestamp(old_commit.commit_time)

    def last_modified(self, path):
        if not self.is_versionned(path):
            return super().last_modified(path)

        if self.repository.status_file(self.from_repo(path)) == pygit2.GIT_STATUS_INDEX_NEW:
            # `path` has been added, but not committed
            return super().last_modified(path)

        path = self.from_repo(path)
        if self._cached_mtime is None:
            self._iter_start()

        # While modification time of `path` is not found, go back in time
        # (commit after commit) until we find a commit involving `path`.
        # Modification times of other files encountered on the way are stored,
        # so that they are retrieved faster the next time.
        while self._cached_mtime[path] is None:
            self._iter_walk()
        return self._cached_mtime[path]

