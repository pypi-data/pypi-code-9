#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from easy_logger.config import DEFAULT_LEVEL, DEFAULT_FORMAT


class Logger(object):

    def __init__(self, level=DEFAULT_LEVEL, format=DEFAULT_FORMAT):
        self._level = level
        self._format = format
        self._formatter = logging.Formatter(self._format)

    def get_logger(self, name):
        return self.get_stream_logger(name)

    def get_stream_logger(self, name):
        """Get logger which has add streamHandler. Output log message to stream.

        :param str name: logger name
        """
        if hasattr(self, 'stream_logger'):
            return self.stream_logger

        logger = logging.getLogger(name)
        logger.setLevel(self._level)

        sh = logging.StreamHandler()
        sh.setFormatter(self._formatter)
        logger.addHandler(sh)

        self.stream_logger = logger
        return self.stream_logger

    def get_file_logger(self, name, filepath):
        """Get logger which has add fileHandler. Output log message to specify file.

        :param str name: logger name
        """
        if hasattr(self, 'file_logger'):
            return self.file_logger

        logger = logging.getLogger(name)
        logger.setLevel(self._level)

        fh = logging.FileHandler(filepath)
        fh.setFormatter(self._formatter)
        logger.addHandler(fh)

        self.file_logger = logger
        return self.file_logger

    def get_both_logger(self, name, filepath):
        """Get logger which has both add streamHandler and fileHandler.
        Output log message to stream and specify file.

        :param str name: logger name
        """
        if hasattr(self, 'both_logger'):
            return self.both_logger

        logger = logging.getLogger(name)
        logger.setLevel(self._level)

        sh = logging.StreamHandler()
        sh.setFormatter(self._formatter)
        logger.addHandler(sh)

        fh = logging.FileHandler(filepath)
        fh.setFormatter(self._formatter)
        logger.addHandler(fh)

        self.both_logger = logger
        return self.both_logger
