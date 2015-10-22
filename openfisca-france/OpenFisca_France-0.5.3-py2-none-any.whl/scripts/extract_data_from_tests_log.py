#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""Extract data from nosetests log.

Use case: create a GitHub issue based on a Travis log.
"""


import argparse
import logging
import os
import sys


app_name = os.path.splitext(os.path.basename(__file__))[0]
log = logging.getLogger(app_name)


def extract_data_from_tests_log(test_log_lines):
    failing_tests = filter(lambda line: line.startswith('FAIL:'), test_log_lines)
    return failing_tests[0]


def main():
    parser = argparse.ArgumentParser(description = __doc__)
    parser.add_argument('log_file', default = False, help = "tests log")
    parser.add_argument('-v', '--verbose', action = 'store_true', default = False, help = "increase output verbosity")
    args = parser.parse_args()
    logging.basicConfig(level = logging.DEBUG if args.verbose else logging.WARNING, stream = sys.stdout)
    with open(args.log_file) as test_log_file:
        test_log_lines = test_log_file.readlines()
    data = extract_data_from_tests_log(test_log_lines)
    print unicode(data).encode('utf-8')
    return 0


if __name__ == "__main__":
    sys.exit(main())
