#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

sys.path.append(os.path.abspath('.'))  # Append 'xxx/easy-logger' to sys.path

from easy_logger import Logger


def test_get_stream_logger():
    logger = Logger().get_stream_logger('test_get_stream_logger')
    logger.info('nihao')


if __name__ == '__main__':
    test_get_stream_logger()
