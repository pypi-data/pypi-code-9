# coding=utf-8
import os
import sys
from unittest import defaultTestLoader, TextTestRunner, TestSuite


TESTS = ("validators", "fields", "forms")


if __name__ == '__main__':
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.abspath(os.path.join(current_dir, '..'))

    if project_dir not in sys.path:
        sys.path.insert(0, project_dir)

    suite = TestSuite()
    suite.addTest(defaultTestLoader.loadTestsFromNames(TESTS))

    runner = TextTestRunner(verbosity=3)
    result = runner.run(suite)
    sys.exit(not result.wasSuccessful())
