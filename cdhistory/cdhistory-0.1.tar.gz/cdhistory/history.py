import collections
import contextlib
import heapq
import logging
import os
import re

logger = logging.getLogger(__name__)


class History(object):
    """
    This class stores a list of paths and the number of times that the user has
    visited each of them. This purpose of this class is to encapsulate the
    matching algorithm that is used to find a particular path.
    """

    def __init__(self, paths):
        """Creates an history object

        Arguments:
            paths - a dict that maps paths on the filesystem to the number of
                    times a user has visited them.

        """
        self.paths = collections.defaultdict(int)
        self.paths.update(paths)

    def add_path(self, path):
        """Add path to the history

        If the path already exists, its value is increased by one. If the path
        is new, its frequency is set to one, and all of the ancestor paths are
        also added with either a frequency of zero or, if they are already in
        the history, with their previous frequency. For example, If the
        following data was contained in the history,

            1 /foo

        and path /foo/bar/baz was added the history would become

            1 /foo
            0 /foo/bar
            1 /foo/bar/baz

        If /foo/bar/baz was added a second time, the history would become,

            1 /foo
            0 /foo/bar
            2 /foo/bar/baz


        Arguments:
            path - a path on the filesystem

        """
        if path == '-':
            path = os.getcwd()

        if not os.path.exists(path):
            raise ValueError("'{}' does not exist".format(path))

        path = os.path.abspath(path)

        try:
            self.paths[path] += 1
        except Exception as e:
            logger.exception(e)
            print(self.paths)
            raise

        while path != "/":
            path = os.path.dirname(path)
            self.paths[path] = self.paths[path]

    def validate(self):
        """Remove any paths the no longer exist on the filesystem"""
        for path in self.paths:
            if not os.path.exists(path):
                logger.debug('removed: {}'.format(path))
                del self.paths[path]

    def matches(self, test, limit=10):
        """Return a list of paths that match the test string

        Arguments:
            test  - the string used to find matching paths
            limit - the maximum number of results to return

        Returns:
            a list of paths

        """
        test = '.*?'.join(re.escape(c) for c in test)
        pattern = re.compile('(?=(' + test + '))')

        # Define a scoring function
        def score(match, path):
            partial = match.end(1) - match.start(1)
            length = len(path) - match.start(1)

            if partial == 0 or length == 0:
                return (0, 0, 0)

            lscore = 1.0 / length
            pscore = 1.0 / partial
            fscore = self.paths[path]
            return (lscore, pscore, fscore)

        # Calculate the score of each path
        results = []
        for path in self.paths:
            matches = [score(m, path) for m in pattern.finditer(path)]
            if matches:
                results.append((max(matches), path))

        # Create a list best match that is not larger that the specified limit
        candidates = [path for _, path in heapq.nlargest(limit, results)]

        if candidates:
            logger.debug('candidates for "{}":'.format(test))
            for candidate in candidates:
                logger.debug('-- {}'.format(candidate))
        else:
            logger.debug('no matches for "{}"'.format(test))

        return candidates

    @classmethod
    def load(cls, filename):
        paths = collections.defaultdict(int)

        with open(filename, 'r') as fp:
            for line in fp:
                try:
                    count, path = line.strip().split(None, 1)

                    # Filter out any  paths that do not exist anymore (these
                    # should not be in the history object for performing
                    # matches on).
                    if os.path.exists(path):
                        paths[path] = int(count)
                        logger.debug('{} {}'.format(count, path))

                except Exception as e:
                    logger.exception(e)

        return cls(paths)

    def save(self, filename):
        # Create a list of (count, path) tuples and sort them into descending
        # order.
        paths = [(c, p) for p, c in self.paths.items()]
        paths.sort(reverse=True)

        with open(filename, 'w') as fp:
            for count, path in paths:
                fp.write('{} {}\n'.format(count, path.strip()))


@contextlib.contextmanager
def history(filename):
    h = History.load(filename)
    yield h
    h.save(filename)
