# encoding: UTF-8
# Copyright (C) 2007-2010, Stefan Schwarzer
# see the file LICENSE for the license of this software

"""
Code for scanning a directory tree and yielding pairs
`(priority, path)`. The first element denotes if the filesystem
path is a directory or a regular file. The type/priority of a link
is derived from the path the link points to.

This module isn't concerned with HTML generation.
"""

import fnmatch
import itertools
import os
import stat
import sys

# Websourcebrowser modules
import coding
import config


class ReadError(Exception):
    pass


def dir_level(path):
    """
    Return the "depth" of a directory, here defined as the number of
    directory separators in the string `path`.
    """
    level = path.count(os.sep)
    if level == 1 and path.endswith(os.sep):
        return 0
    else:
        return level


class DirectoryTree(object):

    def __init__(self, root):
        self.root = os.path.abspath(os.path.normpath(root))

    def walk(self, path, depth=sys.maxint, _max_level=None):
        """
        Return a generator function which recursively yields the items
        (directories and files) with their full paths, starting at the
        root `path`. On each level, the items are sorted with
        directories first, then regular files.

        Each yield gives a tuple (priority, item) where `priority` is 1
        for directories and 2 for files. `item` is a filesystem path.

        If `depth` is given, it's taken for the maximum recursion
        depth of the algorithm, i. e. if `depth` is 1, no recursion is
        done, only the directories and files in `path` are listed. By
        default, the directory `path` with all its nested
        subdirectories is visited.

        Like with `os.walk`, if a directory is really a symbolic link,
        it will be listed but not visited to avoid infinite link
        cycles.
        """
        path = os.path.abspath(path)
        if _max_level is None:
            _max_level = dir_level(path) + depth + 1
        # `listdir` doesn't return items with path separators
        try:
            dirs_and_files = os.listdir(path)
        except OSError:
            return
        # filter out other items than directories and files and add a
        #  priority value for sorting
        for index, item in enumerate(dirs_and_files):
            try:
                joined_path = os.path.join(path, item)
            except UnicodeDecodeError:
                # `path` is supposed to be a unicode string already, so
                #  `item` contains invalid characters
                item = coding.decode(item)
            try:
                item_mode = os.stat(joined_path)[0]
            except OSError:
                # stale link
                priority = 0
                dirs_and_files[index] = (priority, item)
                continue
            if stat.S_ISDIR(item_mode):
                priority = 1
            elif stat.S_ISREG(item_mode):
                priority = 2
            else:
                # ignore sockets, device files etc.
                priority = 0
            # prepend priority value (1 for directories, 2 for files, 0 else)
            dirs_and_files[index] = (priority, item)
        # remove items with priority 0
        dirs_and_files = [item for item in dirs_and_files if item[0]]
        # sort by priority, then basename
        dirs_and_files.sort()
        # yield the sorted items, if necessary, recursively
        for priority, item in dirs_and_files:
            item = os.path.join(path, item)
            yield priority, item
            is_directory = (priority == 1)
            follow_non_link = is_directory and not os.path.islink(item)
            levels_left = (dir_level(item) + 1 < _max_level)
            if is_directory and follow_non_link and levels_left:
                for priority, inner_item in \
                  self.walk(item, _max_level=_max_level):
                    yield priority, inner_item

    def _ignore_item(self, pair):
        """
        Return `True` if the path, the second item in tuple `pair`,
        should be omitted from the list of directories and files,
        else return `False`.
        """
        priority, item = pair
        return config.ignore_path(item)

    def read(self, depth=sys.maxint):
        """
        Read a directory tree `depth` levels deep. A level 1 means
        just the flat directory contents. If the root directory
        (`self.root`) can't be scanned, raise a `ReadError`.

        If the method executes successfully, the instance attribute
        `items` will return a list of the read file system items. The
        items will have the ignore patterns in `config.ignore_patterns`
        already applied. The instance attribute `family` will contain
        a mapping from each item (strings) to an object with the
        attributes `parent`, `previous` and `next`. These are the
        respective items for the parent and the previous and next
        sibling (i. e. previous and next items immediately below the
        same directory). If one of the three paths can't sensibly be
        given, it's set to `None`. Note that the parent directory is
        set to `None` if it's the root directory for the read process.
        """
        if not os.access(self.root, os.R_OK):
            raise ReadError("root '%s' can't be scanned" % self.root)
        # read and filter items
        filtered_items = itertools.ifilterfalse(
          self._ignore_item, self.walk(self.root, depth=depth))
        item_type_map = {1: "directory", 2: "file"}
        self.items = [(item_type_map[priority], item)
                      for (priority, item) in filtered_items]

    def __str__(self):
        return "\n".join(self.items)


if __name__ == '__main__':
    # test code
    config.set_from_environment()
    dt = DirectoryTree(root="/home/schwa/sd/pypy-dist")
    dt.read()

