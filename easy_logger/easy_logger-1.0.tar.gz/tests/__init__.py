#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
import sys
import unittest

sys.path.append(os.path.abspath('.'))  # Append 'xxx/easy-logger' to sys.path

from easy_logger import Logger


class TestEasyLogger(unittest.TestCase):

    def test_get_stream_logger(self):
        logger = Logger().get_stream_logger('test_get_stream_logger')
        logger.info('nihao')

    def test_get_stream_logger_debug_level(self):
        logger = Logger(level=logging.DEBUG).get_stream_logger(
            'test_get_stream_logger_debug_level')
        logger.debug('nihao')

    def test_get_stream_logger_repeat_print(self):
        logger = Logger().get_stream_logger('test_get_stream_logger_repeat_print')

        logger.info('nihao')
        logger.info('nihao')

    def test_get_stream_logger_repeat_call(self):
        logger = Logger().get_stream_logger('test_get_stream_logger_repeat_call')
        logger.info('nihao, 1')

        logger = Logger().get_stream_logger('test_get_stream_logger_repeat_call')
        logger.info('nihao, 2')

        logger = Logger().get_stream_logger('test_get_stream_logger_repeat_call_another_name')
        logger.info('nihao, 3')

    def test_get_file_logger(self):
        logger = Logger().get_file_logger('test_get_file_logger', 'test.log')
        logger.info('nihao')

    def test_get_both_logger(self):
        logger = Logger().get_both_logger('test_get_both_logger', 'test.log')
        logger.info('nihao')


if __name__ == '__main__':
    unittest.main()
