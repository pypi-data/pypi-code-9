import sys
import traceback
import threading
import pytest

# This is modeled off the lucene / carrotsearch thread leak checker and should be in pitaya
@pytest.fixture(scope='function')
def thread_leak_checker(request):

    class ThreadLeakChecker(object):

        def __init__(self):
            self._existing_threads = ThreadLeakChecker._idents(threading.enumerate())
            self._filters = []

        @staticmethod
        def _idents(threads):
            return {t.ident: t for t in threads}

        def _filtered(self, threads):
            return ThreadLeakChecker._idents(t for t in threads if
                                             all(fn(t) for fn in self._filters))

        def add_filter(self, filter):
            """Add a filter that can be used to ignore threads that are uninteresting if they leak

            Parameters
            ----------
            filter : callable(threading.Thread) -> bool
                A function that given a thread returns true if it is to be considered, otherwise false
            """
            self._filters.append(filter)

        def check(self):
            """Check to see if the threads actually stopped in the test, failing if this is not so"""
            current_threads = ThreadLeakChecker._idents(threading.enumerate())

            if set(current_threads.keys()) != set(self._existing_threads.keys()):
                filtered_current = self._filtered(current_threads.values())
                filtered_original = self._filtered(self._existing_threads.values())

                if set(filtered_current.keys()) != set(filtered_original.keys()):
                    outliers = set(filtered_current.keys()).difference(set(filtered_original.keys()))

                    num_outliers = len(outliers)
                    msg = ['%d thread%s leaked from test' % (num_outliers, '' if num_outliers == 1 else 's')]
                    frames = sys._current_frames()
                    for idx, outlier in enumerate(outliers, 1):
                        thrd = current_threads[outlier]
                        msg.append('%d) Thread[id=%s, name=%s, daemon=%s]' %
                                   (idx, thrd.ident, thrd.name, thrd.daemon))
                        try:
                            msg.append('\t'.join(traceback.format_stack(frames[outlier])))
                        except:  # noqa
                            pass

                    pytest.fail('\n'.join(msg))

    checker = ThreadLeakChecker()
    request.addfinalizer(checker.check)
    return checker
